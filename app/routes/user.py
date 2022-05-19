from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.config.database import db
from app.models.user import CreateUserBody, UpdateUserBody, UserResponse
from app.oauth import get_current_user
from app.utils import validate_phone_number, validate_username, validate_password, \
    validate_gender, hash_p
from constants import USERS

user_router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@user_router.get(
    '/',
    response_description="List all users",
    response_model=List[UserResponse]
)
async def get_all_users(
        limit: int = 20,
        skip: int = 0,
):
    users = await db[USERS].find(limit=limit, skip=skip).to_list(None)
    return users


@user_router.get(
    '/{id}',
    response_description="Get a single student",
    response_model=UserResponse
)
async def get_one_user(id: str):
    if (user := await db[USERS].find_one({"_id": id})) is not None:
        return user
    raise HTTPException(status_code=404, detail=f"User: {id} not found")


@user_router.post(
    '/',
    response_description="Add new user",
    response_model=UserResponse
)
async def create_user(user_body: CreateUserBody = Body(...)):
    validate_password(user_body.password)
    validate_phone_number(user_body.phone_number)
    validate_username(user_body.username)
    validate_gender(user_body.gender)

    if (existing_user := await db[USERS].find_one({"username": user_body.username})) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User '{existing_user['username']}' already exists"
        )
    if (existing_user := await db[USERS].find_one({"email": user_body.email})) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email: '{existing_user['email']}' already exists"
        )

    user_body.password = hash_p(user_body.password)
    user_body.following = []
    user_body.followers = []
    user_body.posts = []
    user = jsonable_encoder(user_body)
    new_user = await db[USERS].insert_one(user)
    created_user = await db[USERS].find_one({"_id": new_user.inserted_id})
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=created_user
    )


@user_router.put(
    '/',
    response_description="Update a user",
    response_model=UserResponse
)
async def update_user(
        user_body: UpdateUserBody = Body(...),
        current_user: dict = Depends(get_current_user),
):
    id = current_user["_id"]
    validate_phone_number(user_body.phone_number)
    validate_username(user_body.username)

    user = {k: v for k, v in user_body.dict().items() if v is not None}

    if len(user) >= 1:
        update_result = await db[USERS].update_one({"_id": id}, {"$set": user})
        if update_result.modified_count == 1:
            if (
                    updated_user := await db[USERS].find_one({"_id": id})
            ) is not None:
                return updated_user
    if (existing_user := await db[USERS].find_one({"_id": id})) is not None:
        return existing_user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} not found")


@user_router.delete(
    '/',
    response_description="Delete a student"
)
async def delete_user(
        current_user: dict = Depends(get_current_user),
):
    if current_user is not None:
        delete_result = await db[USERS].delete_one({"_id": current_user["_id"]})

        if delete_result.deleted_count == 1:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User '{current_user['username']}' not found")
