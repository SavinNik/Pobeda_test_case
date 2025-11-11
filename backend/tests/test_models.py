from backend.app.models.user_models import User

def test_user_model():
    """Тестирование модели пользователя"""
    user = User(name="test", email="test@mail.com")
    assert user.name == "test"
    assert user.email == "test@mail.com"

def test_user_repr():
    """Тестирование метода __repr__"""
    user = User(name="test", email="test@mail.com")
    assert repr(user) == "<User test>"
