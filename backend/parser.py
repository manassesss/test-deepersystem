import json
from datetime import datetime
from pymongo import MongoClient
from models import User, UserPreferences
from config import Config

def parse_and_import(json_file: str):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Conectar ao MongoDB
    client = MongoClient(Config.MONGO_URI)
    db = client.get_default_database()
    users_collection = db["users"]

    # Processar cada usuário do JSON
    for user_data in data.get("users", []):
        roles = []
        if user_data.get("is_user_admin"):
            roles.append("admin")
        if user_data.get("is_user_manager"):
            roles.append("manager")
        if user_data.get("is_user_tester"):
            roles.append("tester")

        # Converter a data de criação para timestamp
        created_ts = datetime.fromisoformat(user_data.get("created_at").replace("Z", "+00:00")).timestamp()

        # Criação dos objetos com base nos dataclasses
        preferences = UserPreferences(timezone=user_data.get("user_timezone"))
        user = User(
            username=user_data.get("user"),
            password=user_data.get("password"),
            roles=roles,
            preferences=preferences,
            active=user_data.get("is_user_active", True),
            created_ts=created_ts
        )

        # Inserir no MongoDB
        users_collection.insert_one(user.to_dict())
        print(f"Usuário {user.username} importado com sucesso.")

    print("Importação concluída.")

if __name__ == "__main__":
    parse_and_import("../user.json")