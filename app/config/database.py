import motor.motor_asyncio as motor

import constants
from app.config.env import settings

conn_str = f"mongodb+srv://{settings.cluster_user_name}:{settings.cluster_user_password}@{settings.cluster_name}.fssod.mongodb.net/?retryWrites=true&w=majority"

client = motor.AsyncIOMotorClient(conn_str, serverSelectionTimeoutMS=5000)

try:
    print("Successfully connected. Client info:", client.server_info())
except Exception as e:
    print("Connection failed. Exception:", e)

db = client[settings.database_name]


async def init_db():
    # Get collections in db
    collections_in_dp = await db.list_collection_names()

    # Create collections if not created
    if constants.USERS not in collections_in_dp:
        users = await db.create_collection(
            name=constants.USERS,
            # validator=constants.USERS_VALIDATOR
        )
        print(users)

    if constants.POSTS not in collections_in_dp:
        posts = await db.create_collection(
            name=constants.POSTS,
            # validator=constants.POSTS_VALIDATOR
        )
        print(posts)


# Create an object of GridFs for the above database.
bucket = motor.AsyncIOMotorGridFSBucket(db)
