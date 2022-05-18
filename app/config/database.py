from pymongo import MongoClient

from app.config.env import settings

url = f"mongodb+srv://{settings.cluster_user_name}:{settings.cluster_user_password}@{settings.cluster_name}.fssod.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(url)

ultesa_bb_db = client[settings.database_name]

users = ultesa_bb_db['users']
