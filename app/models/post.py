from pydantic import BaseModel


class CreatePostBody(BaseModel):
    title: str
    content: str