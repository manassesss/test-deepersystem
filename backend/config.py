import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    # Carrega a variável MONGO_URI do arquivo .env ou usa um valor padrão
    MONGO_URI = os.environ.get("MONGO_URI")