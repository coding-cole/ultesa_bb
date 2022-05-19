from fastapi import APIRouter, HTTPException, status, Depends

from app.config.database import db
from app.oauth import get_current_user
from constants import USERS

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
    followed_user = await db[USERS].find_one({"_id": followed_id})
    print()
    current_user_id = current_user["_id"]

    if followed_id == current_user_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Invalid user id"
        )

    if followed_id in current_user["following"]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Already following"
        )

    await db[USERS].update_one(
        {"_id": current_user["_id"]}, {
            "$push": {
                "following": followed_id
            }
        }
    )
    await db[USERS].update_one(
        {"_id": followed_id}, {
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
    unfollowed_user = await db[USERS].find_one({"_id": unfollowed_id})
    current_user_id = current_user["_id"]

    if unfollowed_id == current_user_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Invalid user id"
        )

    if unfollowed_id not in current_user["following"]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Already unfollowed"
        )

    await db[USERS].update_one(
        {"_id": current_user_id}, {
            "$pull": {
                "following": unfollowed_id
            }
        }
    )
    await db[USERS].update_one(
        {"_id": unfollowed_id}, {
            "$pull": {
                "followers": current_user_id
            }
        }
    )
    return f"Unfollowed {unfollowed_user['username']}"
