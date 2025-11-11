from typing import Generator, Dict
import pytest
from flask import Flask
from flask.testing import FlaskClient
from app.database.setup import db
from app.models.user_models import User
from app import create_app


@pytest.fixture(scope="function")
def app() -> Generator[Flask, None, None]:
    """Тестовое приложение с временной базой данных"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app: Flask) -> Generator[FlaskClient, None, None]:
    """Тестовый клиент для HTTP запросов"""
    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture
def user_data() -> Dict[str, str]:
    """Тестовые данные для создания пользователя"""
    return {
        'name': 'newuser',
        'email': 'newuser@gmail.com',
    }