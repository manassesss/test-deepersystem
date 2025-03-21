from flask import Blueprint, jsonify, request, abort
from services.user_service import get_all_users, get_user_by_username, create_user, update_user, delete_user

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route("/users", methods=["GET"])
def list_users():
    """
    Lista todos os usuários
    ---
    responses:
      200:
        description: Lista de usuários
        schema:
          type: array
          items:
            type: object
    """
    users = get_all_users()
    return jsonify(users), 200

@api_bp.route("/users/<username>", methods=["GET"])
def get_user(username):
    """
    Retorna os dados de um usuário específico
    ---
    parameters:
      - name: username
        in: path
        type: string
        required: true
        description: O nome do usuário
    responses:
      200:
        description: Dados do usuário
        schema:
          type: object
      404:
        description: Usuário não encontrado
    """
    user = get_user_by_username(username)
    if not user:
        abort(404, description="Usuário não encontrado")
    return jsonify(user), 200

@api_bp.route("/users", methods=["POST"])
def add_user():
    """
    Cria um novo usuário
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
            password:
              type: string
            roles:
              type: array
              items:
                type: string
            timezone:
              type: string
            active:
              type: boolean
    responses:
      201:
        description: Usuário criado com sucesso
    """
    data = request.get_json()
    if not data:
        abort(400, description="Dados inválidos")
    user = create_user(data)
    return jsonify(user), 201

@api_bp.route("/users/<username>", methods=["PUT"])
def edit_user(username):
    """
    Atualiza os dados de um usuário
    ---
    parameters:
      - name: username
        in: path
        type: string
        required: true
        description: O nome do usuário a ser atualizado
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            password:
              type: string
            roles:
              type: array
              items:
                type: string
            timezone:
              type: string
            active:
              type: boolean
    responses:
      200:
        description: Usuário atualizado com sucesso
      404:
        description: Usuário não encontrado
    """
    data = request.get_json()
    if not data:
        abort(400, description="Dados inválidos")
    user = update_user(username, data)
    if not user:
        abort(404, description="Usuário não encontrado")
    return jsonify(user), 200

@api_bp.route("/users/<username>", methods=["DELETE"])
def remove_user(username):
    """
    Remove um usuário
    ---
    parameters:
      - name: username
        in: path
        type: string
        required: true
        description: O nome do usuário a ser removido
    responses:
      200:
        description: Usuário deletado com sucesso
      404:
        description: Usuário não encontrado
    """
    result = delete_user(username)
    if result.deleted_count == 0:
        abort(404, description="Usuário não encontrado")
    return jsonify({"message": "Usuário deletado com sucesso"}), 200
