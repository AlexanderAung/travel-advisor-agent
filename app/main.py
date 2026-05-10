from uuid import uuid4

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.agent import ask_gemini

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

chat_histories: dict[str, list[dict[str, str]]] = {}


def get_chat_id(request: Request) -> str:
    return request.cookies.get("chat_id") or str(uuid4())


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    chat_id = get_chat_id(request)
    response = templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request, "messages": chat_histories.get(chat_id, [])},
    )
    response.set_cookie("chat_id", chat_id, httponly=True, samesite="lax")
    return response


@app.post("/ask", response_class=HTMLResponse)
async def ask(request: Request, prompt: str = Form(...)):
    chat_id = get_chat_id(request)
    messages = chat_histories.setdefault(chat_id, [])
    messages.append({"role": "user", "content": prompt})

    try:
        answer = await ask_gemini(prompt, session_id=chat_id)
    except Exception as e:
        answer = f"Agent error: {e}"

    messages.append({"role": "agent", "content": answer})

    response = templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request, "messages": messages},
    )
    response.set_cookie("chat_id", chat_id, httponly=True, samesite="lax")
    return response


@app.post("/reset", response_class=HTMLResponse)
async def reset_chat(request: Request):
    chat_id = get_chat_id(request)
    chat_histories.pop(chat_id, None)

    response = templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request, "messages": []},
    )
    response.set_cookie("chat_id", str(uuid4()), httponly=True, samesite="lax")
    return response
