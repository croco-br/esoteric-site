from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from features.tarot.engine import generate_reading
from features.sound.app.main import app as sound_app
from features.oracle.app.main import app as oracle_app
from features.natal.app.main import app as natal_app

ROOT = Path(__file__).resolve().parent
app = FastAPI(title="Casa Arcana", description="Um espaço para explorar símbolos, céu e som.")
templates = Jinja2Templates(directory=ROOT / "templates")

app.mount(
    "/tarot/static",
    StaticFiles(directory=ROOT / "features" / "tarot" / "static"),
    name="tarot-static",
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/site.css", include_in_schema=False)
async def site_stylesheet():
    return FileResponse(ROOT / "site.css", media_type="text/css")


@app.get("/tokens.css", include_in_schema=False)
async def design_tokens():
    return FileResponse(ROOT / "tokens.css", media_type="text/css")


@app.post("/tarot/reading", response_class=JSONResponse)
async def tarot_reading(request: Request):
    payload = await request.json()
    reading_type = payload.get("reading_type")
    try:
        result = generate_reading(reading_type)
    except (KeyError, TypeError):
        raise HTTPException(status_code=422, detail="Tipo de leitura desconhecido")
    for _, card in result["questions_and_cards"]:
        image_path = card.get("image_link", "")
        if image_path.startswith("/static/"):
            card["image_link"] = f"/tarot{image_path}"
    return JSONResponse(content=result)


@app.get("/tarot/", response_class=HTMLResponse)
async def tarot_page(request: Request):
    tarot_templates = Jinja2Templates(directory=ROOT / "features" / "tarot" / "templates")
    return tarot_templates.TemplateResponse(
        "index.html", {"request": request, "static_prefix": "/tarot/static"}
    )


app.mount("/sound", sound_app, name="sound")
app.mount("/oracle", oracle_app, name="oracle")
app.mount("/natal", natal_app, name="natal")
