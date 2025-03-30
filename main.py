from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "SVG TextMorph API is running!"}
