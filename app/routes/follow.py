from bson import ObjectId
from fastapi import APIRouter, HTTPException, status, Depends

from app.config.database import users
from app.oauth import get_current_user
from app.utils import validate_id, check_and_return_user

follow_router = APIRouter(
    prefix="/follow",
    tags=['Follow']
)


@follow_router.post(
    '/follow'
)
async def follow(
        followed_id,
        current_user: dict = Depends(get_current_user)
):
    followed_user = check_and_return_user(followed_id)
    current_user_id = current_user["_id"]

    if followed_id == current_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid user id"
        )

    if followed_id in current_user["following"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Already following"
        )

    users.update_one(
        {"_id": ObjectId(current_user["_id"])}, {
            "$push": {
                "following": followed_id
            }
        }
    )
    users.update_one(
        {"_id": ObjectId(followed_id)}, {
            "$push": {
                "followers": current_user["_id"]
            }
        }
    )
    return f"You now follow {followed_user['username']}"


@follow_router.post(
    '/unfollow'
)
async def unfollow(
        unfollowed_id,
        current_user: dict = Depends(get_current_user)
):
    unfollowed_user = check_and_return_user(unfollowed_id)
    current_user_id = current_user["_id"]

    if unfollowed_id == current_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid user id"
        )

    if unfollowed_id not in current_user["following"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"You're not following this user"
        )

    users.update_one(
        {"_id": ObjectId(current_user_id)}, {
            "$pull": {
                "following": unfollowed_id
            }
        }
    )
    users.update_one(
        {"_id": ObjectId(unfollowed_id)}, {
            "$pull": {
                "followers": current_user_id
            }
        }
    )
    return f"Unfollowed {unfollowed_user['username']}"
