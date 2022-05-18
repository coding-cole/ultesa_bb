from datetime import datetime, timedelta

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.config.env import settings
from app.models.auth import PasswordTokenData, TokenData
from app.utils import check_and_return_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
# SECRET_KEY
# Algorithm
# expiration_time

SECRETE_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
PASSWORD_TOKEN_EXPIRE_MINUTES = settings.password_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRETE_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def create_reset_password_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=PASSWORD_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRETE_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(user_token: str, credentials_exception):
    global token_data
    try:
        payload = jwt.decode(user_token, SECRETE_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception

        token_data = TokenData(id=id)
    except jwt.ExpiredSignatureError:
        HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except JWTError:
        raise credentials_exception

    return token_data


def verify_password_token(password_token: str, credentials_exception):
    try:
        payload = jwt.decode(password_token, SECRETE_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception

        token_data = PasswordTokenData(email=email)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(
    user_token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Token not valid",
        headers={"WWW-Authenticate": "Bearer"}
    )
    token = verify_access_token(user_token, credentials_exception)
    user = check_and_return_user(token.id)

    return user
