from typing import Dict
from flask.testing import FlaskClient


def test_get_all_users_empty(client: FlaskClient) -> None:
    """Тест получения пустого списка пользователей"""
    response = client.get("/api/users")
    assert response.status_code == 200
    assert response.json == []


def test_create_user(client: FlaskClient, user_data: Dict[str, str]) -> None:
    """Тест создания пользователя с валидными данными"""
    response = client.post("/api/users", json=user_data)
    assert response.status_code == 201
    assert response.json["name"] == user_data["name"]
    assert response.json["email"] == user_data["email"]


def test_get_user_by_id(client: FlaskClient, user_data: Dict[str, str]) -> None:
    """Тест получения пользователя по ID"""
    create_response = client.post("/api/users", json=user_data)
    assert create_response.status_code == 201

    user_id = create_response.json["id"]

    get_response = client.get(f"/api/users/{user_id}")
    assert get_response.status_code == 200
    assert get_response.json["name"] == user_data["name"]
    assert get_response.json["email"] == user_data["email"]


def test_create_user_invalid_email(client: FlaskClient) -> None:
    """Тест создания пользователя с невалидным email"""
    response = client.post("/api/users", json={"name": "test", "email": "test"})
    assert response.status_code == 400


def test_get_user_by_invalid_id(client: FlaskClient) -> None:
    """Тест получения пользователя с невалидным ID"""
    response = client.get("/api/users/invalid_id")
    assert response.status_code == 404


def test_create_user_invalid_name(client: FlaskClient) -> None:
    """Тест создания пользователя с пустым именем"""
    response = client.post("/api/users", json={"name": "", "email": "test@gmail.com"})
    assert response.status_code == 400


def test_create_user_duplicate_email(client: FlaskClient, user_data: Dict[str, str]) -> None:
    """Тест создания пользователя с дублирующимся email"""
    # Создаем первого пользователя
    response1 = client.post("/api/users", json=user_data)
    assert response1.status_code == 201
    
    # Пытаемся создать второго с тем же email
    response2 = client.post("/api/users", json=user_data)
    assert response2.status_code == 400
    assert "email уже существует" in response2.json["error"]


def test_create_user_empty_body(client: FlaskClient) -> None:
    """Тест создания пользователя с пустым телом запроса"""
    response = client.post("/api/users", json={})
    assert response.status_code == 400


def test_create_user_invalid_data_type(client: FlaskClient) -> None:
    """Тест создания пользователя с некорректным типом данных"""
    response = client.post("/api/users", json={"name": 123, "email": "test@gmail.com"})
    assert response.status_code in [400, 422]
