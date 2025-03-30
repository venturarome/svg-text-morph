from fastapi import FastAPI, Query, Response
from pydantic import BaseModel
import svgwrite

app = FastAPI()


class User(BaseModel):
    name: str
    age: int

@app.get("/")
def home():
    return {"message": "SVG TextMorph API is running!"}

@app.get("/generate")
def generate(
    words: str = Query(...),
):
    # return {"message": f"Words sent are: {words}."}
    dwg = svgwrite.Drawing(size=("200px", "100px"))
    dwg.add(dwg.text(words, insert=(10, 20), fill='blue'))
    svg = dwg.tostring()
    return Response(content=svg, media_type="image/svg+xml")
