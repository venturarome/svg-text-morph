from fastapi import Depends, FastAPI, Query, Response
from pydantic import BaseModel
import svgwrite

from schemas import (
    AnimationData, animation_data_dependency, 
    FontData, font_data_dependency, 
    Words, words_dependency,
)
from services import ConfigureSvg

app = FastAPI()

@app.get("/")
def home():
    return {"message": "SVG TextMorph API is running!"}

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
