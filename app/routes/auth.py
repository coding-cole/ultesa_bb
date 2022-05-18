from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.config.database import users
from app.models.auth import Token
from app.oauth import create_access_token
from app.utils import verify

auth_router = APIRouter(
    tags=['Authentication']
)


@auth_router.post("/login", response_model=Token)
async def login(
        user_credentials: OAuth2PasswordRequestForm = Depends()
):
    user = users.find_one({"username": user_credentials.username})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User does not exist"
        )

    if not verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Incorrect username or password"
        )

    access_token = create_access_token(
        data={
            "user_id": user.id
        }
    )
    # return token
    return {"access_token": access_token, "token_type": "bearer"}