from typing import List

from fastapi import APIRouter, HTTPException, status, Form, UploadFile, File, Depends
from starlette.responses import JSONResponse

from app.config.database import db
from app.config.firebase import firebase_storage
from app.models.post import PostResponse
from app.oauth import get_current_user
from constants import POSTS, USERS

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
    return posts


@post_router.get(
    '/{id}',
    response_description="Get a single post",
    response_model=PostResponse
)
async def get_one_post(id: str):
    if (user := await db[POSTS].find_one({"_id": id})) is not None:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post: {id} not found")


@post_router.post(
    '/',
    response_description="Add new post",
    response_model=PostResponse
)
async def create_post(
        title: str = Form(...),
        content: str = Form(...),
        image: UploadFile = File(...),
        current_user: dict = Depends(get_current_user),
):
    # TODO: validate title and content length

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
        "image_name": image.filename,
        "comments": [],
        "likes": []
    }

    new_post = await db[POSTS].insert_one(post)
    created_post = await db[POSTS].find_one({"_id": new_post.inserted_id})

    if created_post is not None:
        await db[USERS].update_one(
            {"_id": current_user["_id"]}, {
                "$push": {
                    "posts": created_post["_id"]
                }
            }
        )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=created_post
        )
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Post not created")


@post_router.delete(
    '/{id}',
    response_description="Delete a student"
)
async def delete_user(
        post_id: str,
        current_user: dict = Depends(get_current_user),
):
    # current_user_profile_image_name = current_user["profile_img_name"]
    # TODO: Find a way to delete the existing image before uploading a new one
    # if current_user_profile_image_name is not DEFAULT_PROFILE_IMAGE_NAME:
    #     try:
    #         firebase_storage.delete(name=current_user_profile_image_name, token=firebase_token)
    #     except Exception as e:
    #         raise HTTPException(
    #             status_code=status.HTTP_409_CONFLICT,
    #             detail=f"Unable to delete image: {current_user_profile_image_name} from storage. Error: {e}"
    #         )
    delete_result = await db[POSTS].delete_one({"_id": post_id})
    if delete_result.deleted_count == 1:
        await db[USERS].update_one(
            {"_id": current_user["_id"]}, {
                "$pull": {
                    "posts": post_id
                }
            }
        )
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Post not deleted")

