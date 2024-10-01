from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from fastapi import Request

class CreateUserRequest(BaseModel):
    username: str
    first_name: str
    last_name: str
    full_name: str
    email: EmailStr
    phone_number: str = Field(..., pattern=r'^\+?[1-9]\d{1,14}$')
    password: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str


class Loginform:
    def __init__(self, request: Request):
        self.request: Request = request
        self.email: Optional[str] = None
        self.password: Optional[str] = None

    async def create_auth_form(self):
        form = await self.request.form()
        self.email = form.get("email")
        self.password = form.get("password")
