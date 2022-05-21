from typing import List

from bson import ObjectId
from pydantic import BaseModel, Field

from app.models.object_id import PyObjectId


class PostResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    owner_id: str
    title: str
    content: str
    image_name: str
    comments: List[dict]
    likes: List[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "owner_id": "6287d19f9db4b2d073a722c4",
                "title": "Title of my Post",
                "content": "This content is mostly way too much as this is where everybody want to write a lot"
                           "Yeah and bla bla bla sha",
                "image_name": "posted.png",
                "comments": [
                    {
                        "comment_owner_id": "6287d19f9db4b2d073a722c4",
                        "comment": "Oh i think this is actually nice"
                    },
                    {
                        "comment_owner_id": "6287d19f9db4b2d073a722c4",
                        "comment": "Yeah it is actually nice"
                    }
                ],
                "likes": [
                    "6287d19f9db4b2d073a722c4",
                    "6287d19f9db4b2d073a722c4"
                ]
            }
        }
