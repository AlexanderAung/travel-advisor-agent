# Agent-001

Agent-001 is a small FastAPI web app for chatting with a Gemini-powered travel advisor. The agent helps plan trips by asking for a current location, destination, trip duration, and budget, then returns a concise recommendation with timing, estimated cost, activities, and an alternative destination.

## Features

- Simple chat interface with per-browser chat sessions
- Gemini agent built with Google ADK
- Google Search tool support for current travel information
- Reset button for starting a fresh conversation
- Dockerfile included for container deployment

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- A Google AI Studio API key or Vertex AI environment

## Setup

Install dependencies:

```bash
uv sync
```

Create a `.env` file with one of the supported Google GenAI configurations:

```bash
GOOGLE_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

If you use Vertex AI instead, configure `GOOGLE_CLOUD_PROJECT`; the app will enable Vertex AI automatically and default the location to `us-central1`.

## Run Locally

```bash
uv run uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000` and send a travel request such as:

```text
I am in Yangon and want to visit Tokyo for 5 days with a $1200 budget.
```

## Docker

Build and run the container:

```bash
docker build -t agent-001 .
docker run --env-file .env -p 8080:8080 agent-001
```

Then open `http://127.0.0.1:8080`.

## Project Structure

```text
app/main.py              FastAPI routes and chat session handling
app/agent.py             Gemini travel advisor agent
app/templates/index.html Chat UI template
app/static/style.css     Chat UI styling
Dockerfile               Container image definition
```
