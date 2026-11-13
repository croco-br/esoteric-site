from pathlib import Path

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import (
    HTMLResponse,
)
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles

app = FastAPI()

FEATURE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=FEATURE_DIR / "app" / "templates")
app.mount("/static", StaticFiles(directory=FEATURE_DIR / "app" / "static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "current_page": "index"}
    )
