from bson import ObjectId
from fastapi import APIRouter, HTTPException, status

from app.config.database import users
from app.utils import check_id, check_and_return_user

follow_router = APIRouter(
    prefix="/follow",
    tags=['Follow']
)


@follow_router.post(
    '/'
)
async def follow(current_user_id, followed_id):
    current_user = check_and_return_user(current_user_id)
    followed_user = check_and_return_user(followed_id)

    users.update_one(
        {"_id": ObjectId(current_user_id)}, {
            "$push": {
                "following": followed_id
            }
        }
    )
    users.update_one(
        {"_id": ObjectId(followed_id)}, {
            "$push": {
                "followers": current_user_id
            }
        }
    )
    return f"You now follow {followed_user['username']}"
