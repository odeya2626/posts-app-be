import sys
sys.path.append(".")
import json
import pytest
from .fixtures import client, app, db_session
from fastapi.testclient import TestClient


def test_create_user(client: TestClient)->None:
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


 