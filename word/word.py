from fastapi import APIRouter, Request, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from starlette import status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routers.jwt_handler import get_current_user
from database.basedata import SessionLocal, db_dependency


word_router = APIRouter(
    prefix="/word",
    tags=["word"]
)

templates = Jinja2Templates(directory="templates")


@word_router.get("/", response_class=HTMLResponse)
async def read_all_by_user(request: Request, db: db_dependency):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse("/auth", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse("home.html", {"request": request, "user": user})

