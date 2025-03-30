from fastapi import Depends, FastAPI, Query, Response
from pydantic import BaseModel
import svgwrite

from schemas import FontData, font_data_dependency

app = FastAPI()


class User(BaseModel):
    name: str
    age: int

@app.get("/")
def home():
    return {"message": "SVG TextMorph API is running!"}

@app.get("/generate")
def generate(
    words: str = Query('hello,help'), #TODO after testing, make it mandatory using ellipsis (...)
    show_time: int = Query(1000),
    fade_time: int = Query(1000),
    translation_time: int = Query(1000),
    font: FontData = Depends(font_data_dependency),
):
    dwg = svgwrite.Drawing(size=("200px", "100px"))
    dwg.add(dwg.text(words, insert=(10, 20), fill='blue'))
    svg = dwg.tostring()
    return Response(content=svg, media_type="image/svg+xml")
