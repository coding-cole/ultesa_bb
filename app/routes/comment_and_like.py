from bson import ObjectId
from fastapi import APIRouter, Form, Depends, HTTPException, status

from app.config.database import db
from app.oauth import get_current_user
from constants import POSTS

comment_and_like_router = APIRouter(
    tags=['Comment and Like posts']
)


@comment_and_like_router.post(
    "/comment",
    response_description="Comment on post",
)
async def comment_on_post(
        post_id: str,
        comment: str = Form(...),
        current_user: dict = Depends(get_current_user),
):
    update_result = await db[POSTS].update_one(
        {"_id": ObjectId(post_id)}, {
            "$push": {
                "comments": {
                    "comment_owner_id": current_user["_id"],
                    "comment": comment
                }
            }
        }
    )
    if update_result.modified_count == 1:
        return "Thanks for the comment"
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Unable to make comment")


@comment_and_like_router.post(
    "/like",
    response_description="Like a post",
)
async def like_post(
        post_id: str,
        current_user: dict = Depends(get_current_user),
):
    update_result = await db[POSTS].update_one(
        {"_id": ObjectId(post_id)}, {
            "$push": {
                "likes": current_user["_id"]
            }
        }
    )
    if update_result.modified_count == 1:
        return "Thanks for the like"
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Unable to like this post")
