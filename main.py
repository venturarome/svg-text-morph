from fastapi import Depends, FastAPI, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from schemas import (
    AnimationData, animation_data_dependency, 
    FontData, font_data_dependency, 
    Words, words_dependency,
)
from services import ConfigureSvg

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def welcome_page(request: Request):
    return templates.TemplateResponse("index.html", {'request': request})

@app.get("/generate")
def generate(
    words: Words = Depends(words_dependency),
    font: FontData = Depends(font_data_dependency),
    animation: AnimationData = Depends(animation_data_dependency),
):
    svg_config = ConfigureSvg(words, font, animation)
    return Response(
        content=svg_config.generate(),
        media_type="image/svg+xml"
    )

@app.get("/{catch_all:path}", include_in_schema=False)
async def catch_all_route(catch_all: str):
    return RedirectResponse(url="/")
