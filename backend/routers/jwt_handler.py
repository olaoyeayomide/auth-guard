import os
from datetime import timedelta, datetime
from jose import jwt, JWTError
from fastapi import HTTPException, Request, status
from models import User
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from dotenv import dotenv_values
from dotenv import load_dotenv

ALGORITHM = "HS256"

# Load environment variables
load_dotenv()
# config_credential = dotenv_values(".env")

config_credential = {
    "SECRET_KEY": os.getenv("SECRET_KEY"),
    # "ALGORITHM": "HS256"
}

print("Config Credentials:", config_credential)


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(email: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": email, "id": user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, config_credential["SECRET_KEY"], algorithm=ALGORITHM)


def authenticate_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user or not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


async def get_current_user(request: Request):
    try:
        token = request.cookies.get("access_token")
        if token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication token is missing",
            )

        payload = jwt.decode(
            token, config_credential["SECRET_KEY"], algorithms=[ALGORITHM]
        )
        email: str = payload.get("sub")
        user_id: int = payload.get("id")

        if email is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
            )

        return {"email": email, "id": user_id}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
