import json
from .conftest import user_data

def test_get_all_users_empty(client):
    response = client.get("/api/users")
    assert response.status_code == 200
    assert response.json == []

def test_create_user(client, user_data):
    response = client.post("/api/users", json=user_data)
    assert response.status_code == 201
    assert response.json["name"] == user_data["name"]
    assert response.json["email"] == user_data["email"]

def test_get_user_by_id(client, user_data):
    create_response = client.post("/api/users", json=user_data)
    print(f"Create response: {create_response.data}")
    assert create_response.status_code == 201

    user_id = create_response.json["id"]

    get_response = client.get(f"/api/users/{user_id}")
    assert get_response.status_code == 200
    assert get_response.json["name"] == user_data["name"]
    assert get_response.json["email"] == user_data["email"]

def test_create_user_invalid_email(client):
    response = client.post("/api/users", json={"name": "test", "email": "test"})
    assert response.status_code == 400

def test_get_user_by_invalid_id(client):
    response = client.get("/api/users/invalid_id")
    assert response.status_code == 404

def test_create_user_invalid_name(client):
    response = client.post("/api/users", json={"name": "", "email": "test@mail.com"})
    assert response.status_code == 400
