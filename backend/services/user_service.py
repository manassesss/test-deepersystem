from pymongo import MongoClient
from config import Config
from models import User, UserPreferences
from datetime import datetime

client = MongoClient(Config.MONGO_URI)
db = client.get_default_database()
users_collection = db["users"]

def get_all_users():
    users = list(users_collection.find())
    for user in users:
        # Converte o ObjectId para string
        user['_id'] = str(user['_id'])
    return users

def get_user_by_username(username: str):
    user = users_collection.find_one({"username": username})
    if user:
        user['_id'] = str(user['_id'])
    return user

def create_user(data: dict):
    # Aqui seria interessante validar e converter os dados, possivelmente utilizando os dataclasses
    created_ts = datetime.utcnow().timestamp()
    user = User(
        username=data["username"],
        password=data["password"],
        roles=data.get("roles", []),
        preferences=UserPreferences(timezone=data.get("timezone")),
        active=data.get("active", True),
        created_ts=created_ts
    )
    users_collection.insert_one(user.to_dict())
    return user.to_dict()

def update_user(username: str, data: dict):
    update_data = {}
    if "password" in data:
        update_data["password"] = data["password"]
    if "roles" in data:
        update_data["roles"] = data["roles"]
    if "timezone" in data:
        update_data["preferences.timezone"] = data["timezone"]
    if "active" in data:
        update_data["active"] = data["active"]

    users_collection.update_one({"username": username}, {"$set": update_data})
    return get_user_by_username(username)

def delete_user(username: str):
    return users_collection.delete_one({"username": username})