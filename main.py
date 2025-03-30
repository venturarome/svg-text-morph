from fastapi import Depends, FastAPI, Query, Response
from pydantic import BaseModel
import svgwrite

from schemas import (
    AnimationData, animation_data_dependency, 
    FontData, font_data_dependency, 
    Words, words_dependency,
)

app = FastAPI()


class User(BaseModel):
    name: str
    age: int

@app.get("/")
def home():
    return {"message": "SVG TextMorph API is running!"}

@app.get("/generate")
def generate(
    words: Words = Depends(words_dependency),
    font: FontData = Depends(font_data_dependency),
    animation: AnimationData = Depends(animation_data_dependency),
):
    dwg = svgwrite.Drawing(size=("200px", "100px"))
    dwg.add(dwg.text(words.data, insert=(10, 20), fill='blue'))
    svg = dwg.tostring()
    return Response(content=svg, media_type="image/svg+xml")
