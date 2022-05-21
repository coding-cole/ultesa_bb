from typing import Optional, List

from bson import ObjectId
from fastapi import APIRouter, HTTPException, status, Form, UploadFile, File, Depends
from starlette.responses import JSONResponse

from app.config.database import db
from app.config.firebase import firebase_storage
from app.models.post import post_entity, posts_entity, PostResponse
from app.oauth import get_current_user
from app.constants import POSTS, USERS

post_router = APIRouter(
    prefix="/post",
    tags=['Post']
)


@post_router.get(
    "/",
    response_description="List all Posts",
    response_model=List[PostResponse]
)
async def get_all_posts(
        limit: int = 20,
        skip: int = 0
):
    posts = await db[POSTS].find(limit=limit, skip=skip).to_list(None)
    return posts_entity(posts)


@post_router.get(
    '/{id}',
    response_description="Get a single post",
    response_model=PostResponse
)
async def get_one_post(id: str):
    if (post := await db[POSTS].find_one({"_id": ObjectId(id)})) is not None:
        return post_entity(post)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post: {id} not found")


@post_router.post(
    '/',
    response_description="Add new post",
    response_model=PostResponse
)
async def create_post(
        title: str = Form(...),
        content: str = Form(...),
        image: Optional[UploadFile] = File(...),
        current_user: dict = Depends(get_current_user),
):
    # TODO: validate title and content length
    image_name = None
    if image is not None:
        image_name = image.filename
        # Upload the image first
        try:
            # Upload the new image/file
            firebase_storage.child(f"{image.filename}").put(image.file)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Unable to upload image: {image.filename} to storage. Error: {e}"
            )

    # Create a post
    post = {
        "owner_id": current_user["_id"],
        "title": title,
        "content": content,
        "image_name": image_name,
        "comments": [],
        "likes": []
    }

    new_post = await db[POSTS].insert_one(post)
    created_post = await db[POSTS].find_one({"_id": new_post.inserted_id})

    if created_post is not None:
        await db[USERS].update_one(
            {"_id": current_user["_id"]}, {
                "$push": {
                    "posts": new_post.inserted_id
                }
            }
        )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=post_entity(created_post)
        )
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Post not created")


@post_router.delete(
    '/{id}',
    response_description="Delete a post"
)
async def delete_post(
        id: str,
        current_user: dict = Depends(get_current_user),
):
    post = post_entity(await db[POSTS].find_one({"_id": ObjectId(id)}))

    # Check if user is the owner of the post
    if post["owner_id"] is current_user["_id"]:
        # TODO: Find a way to delete the existing image before uploading a new one
        delete_result = await db[POSTS].delete_one({"_id": ObjectId(id)})

        if delete_result.deleted_count == 1:
            await db[USERS].update_one(
                {"_id": current_user["_id"]}, {
                    "$pull": {
                        "posts": id
                    }
                }
            )
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Unable to delete post")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized")
