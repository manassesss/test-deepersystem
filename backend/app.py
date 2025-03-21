from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from api import api_bp

app = Flask(__name__)
CORS(app)

# Configuração básica do Swagger
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # inclui todas as rotas
            "model_filter": lambda tag: True,  # inclui todos os modelos
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/"
}

Swagger(app, config=swagger_config)

# Registra o blueprint com o prefixo /api
app.register_blueprint(api_bp)

if __name__ == "__main__":
    app.run(debug=True)
