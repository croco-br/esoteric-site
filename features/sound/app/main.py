from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.concurrency import run_in_threadpool

from features.static_url import fingerprinted
from features.sound.app.engine import generate_audio

app = FastAPI()

FEATURE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=FEATURE_DIR / "app" / "templates")
app.mount("/static", StaticFiles(directory=FEATURE_DIR / "app" / "static"), name="static")


templates.env.globals["static_url"] = fingerprinted(FEATURE_DIR / "app" / "static", "sound:static")


@app.get("/", response_class=HTMLResponse)
@app.get("/chakras", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "chakras.html", {"request": request, "current_page": "chakras"}
    )


@app.get("/frequencies", response_class=HTMLResponse)
async def render_tab2(request: Request):
    return templates.TemplateResponse(
        "frequencies.html", {"request": request, "current_page": "frequencies"}
    )


@app.get("/audio/{note_name}")
async def get_audio(note_name: str):
    # Synthesis + WAV encoding are CPU-bound; keep them off the event loop.
    audio_buffer = await run_in_threadpool(generate_audio, note_name)
    if audio_buffer is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return StreamingResponse(
        audio_buffer,
        media_type="audio/wav",
        headers={"Cache-Control": "public, max-age=86400"},  # immutable per note
    )
