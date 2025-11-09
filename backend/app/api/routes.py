from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from backend.app.models.user_models import User
from backend.app.schemas.user_schemas import UserCreate
from backend.app.database.setup import db

api = Blueprint("api", __name__)


@api.route("/users", methods=["GET"])
def get_all_users():
    try:
        users = User.query.all()
        return jsonify([user.dict() for user in users])
    except Exception as e:
        return jsonify({"error": "Пользователи не найдены"}), 500


@api.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id: int):
    try:
        user = User.query.get_or_404(user_id)
        return jsonify(user.dict())
    except Exception as e:
        return jsonify({"error": "Пользователь не найден"}), 404


@api.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        validated_data = UserCreate(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": "Неверные данные"}), 400

    try:
        user = User(
            name=validated_data.name,
            email=validated_data.email
        )
        db.session.add(user)
        db.session.commit()
        return jsonify(user.dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Не удалось создать пользователя"}), 500






















