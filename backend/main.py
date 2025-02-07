from pathlib import Path
from fastapi import FastAPI
from routers.auth import router
from word.word import word_router
from starlette.staticfiles import StaticFiles

app = FastAPI()

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of main.py
# STATIC_DIR = os.path.join(BASE_DIR, "..", "frontend", "static")

# if not os.path.exists(STATIC_DIR):
#     os.makedirs(STATIC_DIR)  # Create the directory if it doesn't exist

# app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

STATIC_DIR = Path(__file__).resolve().parent.parent / "frontend" / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)  # Ensure it exists

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


app.include_router(router)
app.include_router(word_router)
