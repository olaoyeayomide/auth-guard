import sys
import os
from pathlib import Path
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routers.auth import router
from word.word import word_router


app = FastAPI()

STATIC_DIR = Path(__file__).resolve().parent / "../frontend/static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


app.include_router(router)
app.include_router(word_router)
