import bson
from bson import ObjectId
from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.config.database import users

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


def serialise_dict(a) -> dict:
    return {**{i: str(a[i]) for i in a if i == '_id'}, **{i: a[i] for i in a if i != '_id'}}


def serialise_list(entity) -> list:
    return [serialise_dict(a) for a in entity]


def check_id(id):
    if not bson.objectid.ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid id"
        )


def check_and_return_user(id):
    check_id(id)
    existing_user_with_id = users.find_one({"_id": ObjectId(id)})
    if not existing_user_with_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User does not exist"
        )
    return serialise_dict(existing_user_with_id)
