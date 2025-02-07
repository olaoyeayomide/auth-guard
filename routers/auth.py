from fastapi import APIRouter, Depends, Request, Response, status, Form, BackgroundTasks
from jose import jwt, JWTError
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Annotated
from routers.jwt_handler import authenticate_user, create_access_token
from routers.email_handler import send_reset_email
from models import User
from schemas.auth_schemas import CreateUserRequest, Token, Loginform
from datetime import timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from database.basedata import db_dependency
from dotenv import dotenv_values
from dotenv import load_dotenv

router = APIRouter(prefix="/auth", tags=["auth"])

templates = Jinja2Templates(directory="/frontend/templates")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Load environment variables
load_dotenv()
config_credential = dotenv_values(".env")


# User Creation
@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest, db: db_dependency):
    create_user_model = User(
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        full_name=create_user_request.full_name,
        email=create_user_request.email,
        phone_number=create_user_request.phone_number,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        role=create_user_request.role,
        is_active=True,
    )

    db.add(create_user_model)
    db.commit()

    return create_user_model


# Login and Token Generation


@router.post("/token", response_model=Token)
async def login_for_access_token(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency,
):
    user = authenticate_user(form_data.email, form_data.password, db)

    if not user:
        return False

    token = create_access_token(user.email, user.id, timedelta(minutes=60))
    response.set_cookie(key="access_token", value=token, httponly=True)

    return True


# Login Page
@router.get("/", response_class=HTMLResponse)
async def authenticationpage(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# Login Processing
@router.post("/", response_class=HTMLResponse)
async def login(request: Request, db: db_dependency):
    form = Loginform(request)
    await form.create_auth_form()
    response = RedirectResponse(url="/word", status_code=status.HTTP_302_FOUND)

    validate_user_cookie = await login_for_access_token(
        response=response, form_data=form, db=db
    )

    if not validate_user_cookie:
        msg = "Invalid username or password"
        return templates.TemplateResponse(
            "login.html", {"request": request, "msg": msg}
        )
    return response


@router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    msg = "Logout successful"
    response = templates.TemplateResponse(
        "login.html", {"request": request, "msg": msg}
    )
    response.delete_cookie(key="access_token")
    return response


# PASSWORD RESET
@router.post("/forgotten_password", response_class=HTMLResponse)
async def forgotten_password_post(
    request: Request,
    background_tasks: BackgroundTasks,
    db: db_dependency,
    email: str = Form(...),
):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        msg = "Email not found"
        return templates.TemplateResponse(
            "password_reset.html", {"request": request, "msg": msg}
        )

    # Create a reset token (e.g., JWT or unique random token)
    token = create_access_token(user.email, user.id, timedelta(hours=1))

    # Send password reset email (assuming send_reset_email is defined)
    background_tasks.add_task(send_reset_email, email, token)

    msg = "Password reset link sent to your email"
    return templates.TemplateResponse(
        "password_reset.html", {"request": request, "msg": msg}
    )


@router.get("/forgotten_password", response_class=HTMLResponse)
async def forgotten_password_form(request: Request):
    return templates.TemplateResponse("password_reset.html", {"request": request})


@router.get("/reset_password/{token}", response_class=HTMLResponse)
async def reset_password_form(request: Request, token: str):
    return templates.TemplateResponse(
        "password_reset_form.html", {"request": request, "token": token}
    )


@router.post("/reset_password/{token}", response_class=HTMLResponse)
async def reset_password(
    request: Request,
    token: str,
    db: db_dependency,
    new_password: str = Form(...),
    new_password2: str = Form(...),
):
    if new_password != new_password2:
        msg = "Passwords do not match"
        return templates.TemplateResponse(
            "password_reset_form.html", {"request": request, "msg": msg, "token": token}
        )

    try:
        # Decode the token
        payload = jwt.decode(
            token, config_credential["SECRET_KEY"], algorithms=["HS256"]
        )
        email = payload.get("sub")
        user_id = payload.get("id")

        if not email or not user_id:
            msg = "Invalid token"
            return templates.TemplateResponse(
                "password_reset_form.html",
                {"request": request, "msg": msg, "token": token},
            )

        # Fetch the user and update the password
        user = db.query(User).filter(User.id == user_id).first()
        user.hashed_password = bcrypt_context.hash(new_password)
        db.commit()

        msg = "Password reset successfully"
        return templates.TemplateResponse(
            "login.html", {"request": request, "msg": msg}
        )

    except JWTError:
        msg = "Invalid or expired token"
        return templates.TemplateResponse(
            "password_reset_form.html", {"request": request, "msg": msg, "token": token}
        )


@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register", response_class=HTMLResponse)
async def register_user(
    request: Request,
    db: db_dependency,
    username: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    full_name: str = Form(...),
    email: str = Form(...),
    phone_number: str = Form(...),
    password: str = Form(...),
    password2: str = Form(...),
    role: str = Form(...),
):

    validation1 = db.query(User).filter(User.username == username).first()
    validation2 = db.query(User).filter(User.email == email).first()

    if password != password2 or validation1 is not None or validation2 is not None:
        msg = "Invalid input"
        return templates.TemplateResponse(
            "register.html", {"request": request, "msg": msg}
        )

    user_model = User()
    user_model.username = username
    user_model.first_name = first_name
    user_model.last_name = last_name
    user_model.full_name = full_name
    user_model.email = email
    user_model.phone_number = phone_number
    user_model.hashed_password = bcrypt_context.hash(password)
    user_model.role = role
    user_model.is_active = True

    db.add(user_model)
    db.commit()

    msg = "Register successfully"
    return templates.TemplateResponse("login.html", {"request": request, "msg": msg})
