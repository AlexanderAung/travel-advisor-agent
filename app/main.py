from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.agent import ask_gemini

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"request": request, "answer": None}
    )


@app.post("/ask", response_class=HTMLResponse)
async def ask(request: Request, prompt: str = Form(...)):

    try:
        answer = await ask_gemini(prompt)
    except Exception as e:
        answer = f"Agent error: {e}"

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request, "answer": answer, "prompt": prompt},
    )
