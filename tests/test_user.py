import sys

sys.path.append(".")

from fastapi.testclient import TestClient

from .fixtures import app, client, db_session


def test_create_user(client: TestClient) -> None:
    response = client.post(
        "/user/register",
        json={
            "username": "testuser",
            "email": "test@test.com",
            "password": "testpassword",
        },
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@test.com"
