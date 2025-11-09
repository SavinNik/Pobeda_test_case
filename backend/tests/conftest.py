import pytest
from backend.app.database.setup import db
from backend.app.models.user_models import User
from backend.app import create_app


@pytest.fixture(scope="function")
def app():
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
def client(app):
    """Тестовый клиент для HTTP запросов"""
    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture
def user(app):
    """Тестовый пользователь"""
    with app.app_context():
        user = User(
            name='testuser',
            email='user@gmail.com',
        )
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture
def user_data():
    """Тестовые данные для создания пользователя"""
    return {
        'name': 'newuser',
        'email': 'newuser@gmail.com',
    }