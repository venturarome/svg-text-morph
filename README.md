# svg-text-morph
Create SVG files with amazingly animated text



## Project setup
1. On the root folder, it is recommended to use `venv` so the dependencies are kept isolate:
```bash
python3 -m venv venv
source venv/bin/activate
```
2. Install required libraries:
```bash
pip install -r requirements.txt
```
Libraries explanation (if someone needs it):
  - fastapi: the web framework.
  - uvicorn: a lightweight server to run FastAPI app.
  - svgwrite: a library for easy SVG generation.
3. Run the server:
```bash
uvicorn main:app --reload
```
4. You can access the API at `http://localhost:8000` and its documentation at `http://localhost:8000/docs`.
5. Whenever you want to finish vorking on it:
   - Stop the server (CTRL+C).
   - Exit the virtual environment by running `deactivate`.
