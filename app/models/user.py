from pydantic import BaseModel, EmailStr
from typing import List, Optional


class CreateUserBody(BaseModel):
    email: EmailStr
    first_name: str
    middle_name: str
    last_name: str
    school: str
    department: str
    gender: str
    phone_number: str
    username: str
    password: str


class UpdateUserBody(BaseModel):
    email: EmailStr
    profile_img: str
    school: str
    department: str
    phone_number: str
    username: str
