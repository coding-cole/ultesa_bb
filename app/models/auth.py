from typing import Optional

from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class ResetPassword(BaseModel):
    new_password: str
    confirm_password: str


class ResetPasswordBody(BaseModel):
    password: str


class PasswordTokenData(BaseModel):
    email: Optional[str] = None
