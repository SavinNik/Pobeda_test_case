import logging
from ..database.setup import db
from ..models.user_models import User
from ..schemas.user_schemas import UserResponse, UserCreate
from typing import List

logger = logging.getLogger(__name__)


def get_users() -> List[UserResponse]:
    """Получить список всех пользователей"""
    users = db.session.execute(db.select(User)).scalars().all()
    return [UserResponse.model_validate(user) for user in users]


def get_user(user_id: int) -> UserResponse:
    """Получить пользователя по ID"""
    user = db.session.get(User, user_id)
    if not user:
        raise ValueError(f"Пользователь с ID {user_id} не найден")
    return UserResponse.model_validate(user)


def create_user(user_data: UserCreate) -> UserResponse:
    """Создать нового пользователя"""
    existing_user = db.session.execute(
        db.select(User).filter_by(email=user_data.email)
    ).scalar_one_or_none()

    if existing_user:
        raise ValueError("Пользователь с таким email уже существует")

    try:
        user = User(
            name=user_data.name,
            email=user_data.email
        )
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return UserResponse.model_validate(user)
    except Exception as e:
        db.session.rollback()
        raise
