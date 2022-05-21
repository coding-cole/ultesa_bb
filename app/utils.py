import re

from fastapi import HTTPException, status
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_p(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def check_user(current_user, id):
    # If user not logged in as admin or normal user raise HTTPException
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Not authenticated, Login"
        )
    if current_user.id != id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Not authenticated, Login"
        )


def validate_password(password):
    if not re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid password"
        )


def validate_phone_number(number):
    if not re.fullmatch(r'[0-9+]{11,14}', str(number)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid phone number"
        )


def validate_username(username):
    if not re.fullmatch(r'[a-zA-Z0-9._]{6,30}(?!.*[_.]{2})$', username):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid username"
        )


def validate_gender(gender):
    if not re.fullmatch(r'[mf]', gender):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid gender"
        )
