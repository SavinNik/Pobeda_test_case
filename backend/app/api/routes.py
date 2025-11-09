from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from backend.app.models.user_models import User
from backend.app.schemas.user_schemas import UserCreate, UserResponse
from backend.app.database.setup import db

api = Blueprint("api", __name__)


@api.route("/users", methods=["GET"])
def get_all_users():
    try:
        users = db.session.execute(db.select(User)).scalars().all()
        users_response = [UserResponse.model_validate(user).model_dump() for user in users]
        return jsonify(users_response)
    except Exception as e:
        return jsonify({"error": "Пользователи не найдены"}), 500


@api.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id: int):
    try:
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({"error": "Пользователь не найден"}), 404
        user_response = UserResponse.model_validate(user)
        return jsonify(user_response.model_dump())
    except Exception as e:
        return jsonify({"error": "Ошибка при получении пользователя"}), 500


@api.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.get_json()

        if not data or not isinstance(data, dict):
            return jsonify({"error": "Неверный формат данных"}), 400

        if not data.get("name") or not data.get("email"):
            return jsonify({"error": "Неверные данные: имя и email обязательны"}), 400

        try:
            validated_data = UserCreate(**data)
        except ValidationError as e:
            print(f"Validation error: {e}")
            return jsonify({"error": f"Ошибка валидации: {str(e)}"}), 400

        if User.query.filter_by(email=validated_data.email).first():
            return jsonify({"error": "Пользователь с таким email уже существует"}), 400

        user = User(
            name=validated_data.name,
            email=validated_data.email
        )
        db.session.add(user)
        db.session.commit()

        user_response = UserResponse.model_validate(user)
        return jsonify(user_response.model_dump()), 201

    except Exception as e:
        db.session.rollback()
        print(f"Unexpected error in create_user: {str(e)}")
        return jsonify({"error": "Внутренняя ошибка сервера"}), 500






















