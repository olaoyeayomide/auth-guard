from fastapi import FastAPI
from routers.auth import router
from word.word import word_router
from starlette.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)
app.include_router(word_router)