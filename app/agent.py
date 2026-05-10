import os
from uuid import uuid4

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai.types import Content, Part

load_dotenv(override=True)


APP_USER_ID = "travel_advisor_web"

session_service = InMemorySessionService()


def configure_genai_environment() -> None:
    if os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_GENAI_USE_VERTEXAI"):
        return

    if os.getenv("GOOGLE_CLOUD_PROJECT"):
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "1"
        os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")


def create_agent() -> Agent:
    return Agent(
        name="travel_advisor",
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        description=(
            "A simple travel advisor that recommends the best time to visit, "
            "estimated budget, fun things to do, and an alternative destination "
            "based on the user's location, destination, trip duration, and budget."
        ),
        instruction="""
You are a practical travel advisor.

Mission:
Help the user plan a trip using only these inputs:
1. current location
2. destination
3. trip duration
4. budget

Your job:
- Recommend the best time to visit the destination.
- Estimate a realistic budget for the trip duration.
- Suggest a few fun things to do there.
- Suggest one alternative destination that fits a similar budget.

Rules:
- Use clear simple sentences.
- Do not give too many options.
- Give useful travel advice, not general travel theory.
- If the user did not give all inputs, ask only for the missing one(s).
- Use Google Search to check current travel information when needed.
- Prefer practical advice over perfect detail.
- If exact prices are uncertain, give a rough budget range and say it is estimated.
- Base the recommendation on the user's trip duration and likely travel cost from their current location.
- Mention the alternative destination in one short paragraph or 1-2 short bullets.
- Keep the tone helpful, confident, and concise.

Response format:
1. Best time to visit
2. Estimated budget
3. Fun things to do
4. Alternative destination

Each section should be short.
""",
        tools=[google_search],
    )


configure_genai_environment()
agent = create_agent()
runner = Runner(
    agent=agent,
    session_service=session_service,
    app_name=agent.name,
)


async def ask_gemini(prompt: str, session_id: str | None = None) -> str:
    session_id = session_id or str(uuid4())
    session = await session_service.get_session(
        app_name=agent.name,
        user_id=APP_USER_ID,
        session_id=session_id,
    )

    if session is None:
        session = await session_service.create_session(
            app_name=agent.name,
            user_id=APP_USER_ID,
            session_id=session_id,
        )

    final_response = ""
    try:
        async for event in runner.run_async(
            user_id=APP_USER_ID,
            session_id=session.id,
            new_message=Content(parts=[Part(text=prompt)], role="user"),
        ):
            if event.is_final_response() and event.content and event.content.parts:
                final_response = event.content.parts[0].text or ""
    except Exception as exc:
        return f"Agent error: {exc}"

    if final_response.strip():
        return final_response.strip()

    return "No response text returned by the agent."
