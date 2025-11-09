from backend.app.models.user_models import User

def test_user_model():
    user = User(name="test", email="test@mail.com")
    assert user.name == "test"
    assert user.email == "test@mail.com"

def test_user_repr():
    user = User(name="test", email="test@mail.com")
    assert repr(user) == "<User test>"

def test_user_dict():
    user = User(name="test", email="test@mail.com")
    assert user.dict() == {"id": None, "name": "test", "email": "test@mail.com"}