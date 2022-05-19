import motor.motor_asyncio
from pymongo import MongoClient
import gridfs
from app.config.env import settings

url = f"mongodb+srv://{settings.cluster_user_name}:{settings.cluster_user_password}@{settings.cluster_name}.fssod.mongodb.net/?retryWrites=true&w=majority"

# connection = MongoClient(url)
#
# db = connection[settings.database_name]
client = motor.motor_asyncio.AsyncIOMotorClient(url)

db = client[settings.database_name]

# Create an object of GridFs for the above database.
fs = motor.motor_asyncio.AsyncIOMotorGridFSBucket(db)
