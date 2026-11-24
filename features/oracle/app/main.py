from pathlib import Path

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import (
    HTMLResponse,
)
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles

from features.static_url import fingerprinted

app = FastAPI()

FEATURE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = FEATURE_DIR / "app" / "static"
templates = Jinja2Templates(directory=FEATURE_DIR / "app" / "templates")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


templates.env.globals["static_url"] = fingerprinted(STATIC_DIR, "oracle:static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "current_page": "index"}
    )
