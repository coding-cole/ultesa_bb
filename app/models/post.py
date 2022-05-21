from typing import List

from bson import ObjectId
from pydantic import BaseModel


class PostResponse(BaseModel):
    id: str
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


def post_entity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "owner_id": item["owner_id"],
        "title": item["title"],
        "content": item["content"],
        "image_name": item["image_name"],
        "comments": item["comments"],
        "likes": item["likes"]
    }


def posts_entity(entity) -> list:
    return [post_entity(item) for item in entity]
