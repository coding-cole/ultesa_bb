from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field

from app.models.object_id import PyObjectId
from constants import DEFAULT_PROFILE_IMAGE_NAME


class CreateUserBody(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr = Field(...)
    first_name: str = Field(...)
    middle_name: str = Field(...)
    last_name: str = Field(...)
    school: str = Field(...)
    department: str = Field(...)
    gender: str = Field(...)
    phone_number: str = Field(...)
    username: str = Field(...)
    password: str = Field(...)
    profile_img_name: str = DEFAULT_PROFILE_IMAGE_NAME
    verified: bool = False
    following: List[str]
    followers: List[str]
    posts: List[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "email": "jdoe@example.com",
                "first_name": "Jane",
                "middle_name": "Doe",
                "last_name": "Cole",
                "school": "UNILAG",
                "department": "Maths",
                "gender": "m",
                "phone_number": "08187706081",
                "username": "john_doe",
                "password": "password123",
                "profile_img_name": DEFAULT_PROFILE_IMAGE_NAME,
                "verified": False,
                "following": [],
                "followers": [],
                "posts": []
            }
        }


class UpdateUserBody(BaseModel):
    email: Optional[EmailStr]
    school: Optional[str]
    department: Optional[str]
    phone_number: Optional[str]
    username: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "email": "jdoe@example.com",
                "school": "UNILAG",
                "department": "Maths",
                "phone_number": "08187706081",
                "username": "john_doe",
            }
        }


class UserResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr
    first_name: str
    middle_name: str
    last_name: str
    school: str
    department: str
    gender: str
    phone_number: str
    username: str
    profile_img_name: str
    verified: bool
    following: List[str]
    followers: List[str]
    posts: List[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
