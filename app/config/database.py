import asyncio

import motor.motor_asyncio as motor

from app.config.env import settings

conn_str = f"mongodb+srv://{settings.cluster_user_name}:{settings.cluster_user_password}@{settings.cluster_name}.fssod.mongodb.net/?retryWrites=true&w=majority"

client = motor.AsyncIOMotorClient(conn_str, serverSelectionTimeoutMS=5000)

try:
    print("Successfully connected. Client info:", client.server_info())
except Exception as e:
    print("Connection failed. Exception:", e)

db = client[settings.database_name]

# Create an object of GridFs for the above database.
bucket = motor.AsyncIOMotorGridFSBucket(db)
