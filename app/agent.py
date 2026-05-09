from google import genai
from typing import Optional
from dotenv import load_dotenv
from google.genai import errors as genai_errors
import os

load_dotenv()


# create gemini client
def ask_gemini(prompt: str) -> str:

    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL") or "gemini-2.0-flash"

    if not api_key:
        raise RuntimeError("Missing GEMINI_API_KEY!")

    client = genai.Client(api_key=api_key)
    try:
        response = client.models.generate_content(model=model, contents=prompt)
    except genai_errors.ClientError as e:
        return f"Gemini API error: {e}"

    text: Optional[str] = getattr(response, "text", None)
    if text and text.strip():
        return text.strip()

    return "No response text returned by the model."
