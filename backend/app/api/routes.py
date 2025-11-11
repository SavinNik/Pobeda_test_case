from typing import Tuple
from flask import Blueprint, request, jsonify, Response
from pydantic import ValidationError

from ..schemas.user_schemas import UserCreate
from ..api.crud import get_users, get_user, create_user


api = Blueprint("api", __name__)

@api.route("/users", methods=["GET"])
def get_all_users_route() -> Tuple[Response, int]:
    """Получить список всех пользователей"""
    try:
        users = get_users()
        users_data = [user.model_dump() for user in users]
        return jsonify(users_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id_route(user_id: int) -> Tuple[Response, int]:
    """Получить пользователя по ID"""
    try:
        user = get_user(user_id)
        return jsonify(user.model_dump()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route("/users", methods=["POST"])
def create_user_route():
    """Создать нового пользователя"""
    json_data = request.get_json()

    if not json_data:
        return jsonify({"error": "Не переданы данные"}), 400

    try:
        user_data = UserCreate.model_validate(json_data)
        user = create_user(user_data)
        return jsonify(user.model_dump()), 201
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        return jsonify({"error": "Внутренняя ошибка сервера"}), 500












