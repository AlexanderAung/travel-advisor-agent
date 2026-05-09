import os
from vertexai import init
from vertexai.generative_models import GenerativeModel
from dotenv import load_dotenv

load_dotenv(override=True)


# create gemini client
def ask_gemini(prompt: str) -> str:
    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    if not project:
        raise RuntimeError("Missing GOOGLE_CLOUD_PROJECT!!")

    init(project=project, location=location)
    model = GenerativeModel(model)

    try:
        response = model.generate_content(contents=prompt)
    except Exception as e:
        return f"Vertex API error: {e}"

    text = getattr(response, "text", None)
    if text and text.strip():
        return text.strip()

    return "No response text returned by the model."
