from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Body, UploadFile, File
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.config.database import db
from app.config.firebase import firebase_storage, firebase_token
from app.models.user import CreateUserBody, UpdateUserBody, UserResponse
from app.oauth import get_current_user
from app.utils import validate_phone_number, validate_username, validate_password, \
    validate_gender, hash_p
from constants import USERS, DEFAULT_PROFILE_IMAGE_NAME

user_router = APIRouter(
    prefix="/user",
    tags=['User']
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
    response_description="Get a single user",
    response_model=UserResponse
)
async def get_one_user(id: str):
    if (user := await db[USERS].find_one({"_id": id})) is not None:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User: {id} not found")


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

    user = {k: v for k, v in user_body.dict().items() if v is not None}

    if len(user) >= 1:
        update_result = await db[USERS].update_one({"_id": id}, {"$set": user})
        if update_result.modified_count == 1:
            updated_user = await db[USERS].find_one({"_id": id})
            return updated_user
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Unable to make changes")

    return current_user


@user_router.post(
    '/update_profile_image',
    response_description="Update a user profile image",
)
async def update_profile_image(
        file: UploadFile = File(...),
        current_user: dict = Depends(get_current_user),
):
    id = current_user["_id"]
    current_user_profile_image_name = current_user["profile_img_name"]

    if current_user_profile_image_name is not file.filename:
        # TODO: Find a way to delete the existing image before uploading a new one

        # Upload the new image/file
        try:
            # Upload the new image/file
            firebase_storage.child(f"{file.filename}").put(file.file)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Unable to upload image: {file.filename} to storage. Error: {e}"
            )
        # Update the uploaded image/file name in user db
        update_result = await db[USERS].update_one({"_id": id}, {"$set": {"profile_img_name": file.filename}})
        # Get updated user and return
        if update_result.modified_count == 1:
            updated_user = await db[USERS].find_one({"_id": id})
            return updated_user
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Unable to upload image")
    return current_user


@user_router.delete(
    '/',
    response_description="Delete a student")
async def delete_user(
        current_user: dict = Depends(get_current_user),
):
    # TODO: Find a way to delete the existing image before uploading a new one
    delete_result = await db[USERS].delete_one({"_id": current_user["_id"]})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Unable to delete user")