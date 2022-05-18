from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from app.config.database import users
from app.models.user import CreateUserBody, UpdateUserBody
from app.oauth import get_current_user
from app.utils import serialise_list, hash_p, check_and_return_user, \
    validate_phone_number, validate_username, validate_password, validate_gender

user_router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@user_router.get(
    '/',
    # response_model=List[UserResponse]
)
async def get_all_users(
        limit: int = 20,
        skip: int = 0,
):
    return serialise_list(users.find().limit(limit).skip(skip))


@user_router.get(
    '/{id}',
)
async def get_one_user(id):
    user = check_and_return_user(id)
    return user


@user_router.post(
    '/',
)
async def create_user(user_body: CreateUserBody):
    validate_password(user_body.password)
    validate_phone_number(user_body.phone_number)
    validate_username(user_body.username)
    validate_gender(user_body.gender)

    existing_user_with_username = users.find_one({"username": user_body.username})
    if existing_user_with_username is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Account with username: '{user_body.username}' already exists "
        )

    existing_user_with_email = users.find_one({"email": user_body.email})
    if existing_user_with_email is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Account with email: '{user_body.email}' already exists "
        )

    new_user = {
        "email": user_body.email,
        "first_name": user_body.first_name.lower(),
        "middle_name": user_body.middle_name.lower(),
        "last_name": user_body.last_name.lower(),
        "school": user_body.school.lower(),
        "department": user_body.department.lower(),
        "gender": user_body.gender.lower(),
        "phone_number": user_body.phone_number,
        "username": user_body.username,
        "password": hash_p(user_body.password),
        # insert by default
        "profile_img": "blablablas",
        "verified": False,
        "following": [],
        "followers": [],
        "posts": []
    }
    users.insert_one(new_user)
    return "User created"


@user_router.put(
    '/',
)
async def update_user(
        user_body: UpdateUserBody,
        current_user: dict = Depends(get_current_user),
):
    id = current_user["_id"]
    validate_phone_number(user_body.phone_number)
    validate_username(user_body.username)
    check_and_return_user(id)

    users.update_one(
        {"_id": ObjectId(id)},
        {"$set": dict(user_body)}
    )
    return check_and_return_user(id)


@user_router.delete('/')
async def delete_user(
        current_user: dict = Depends(get_current_user),
):
    id = current_user["_id"]
    username = check_and_return_user(id)["username"]
    users.delete_one({"_id": ObjectId(id)})
    return f"Your account: '{username}' was deleted successfully"
