import sys
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.routers.auth import router
from backend.word.word import word_router

app = FastAPI()

# Add CORS middleware to allow cross-origin requests from your frontend (Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://auth-guard-black.vercel.app>"
    ],  # Replace with your actual Vercel frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

STATIC_DIR = Path(__file__).resolve().parent / "../frontend/static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Include your routers
app.include_router(router)
app.include_router(word_router)
