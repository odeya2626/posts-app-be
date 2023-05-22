import sys
sys.path.append(".")
import json
import pytest
from .fixtures import client, app, db_session
from fastapi.testclient import TestClient
from db.db_post import create

valid_post = {
            "img_url": "https://www.google.com",
            "img_url_type": "absolute",
            "caption": "test caption",
            "creator_id": 1,
        }

def test_create_post_success(client: TestClient)->None:
    response = client.post(
        "/post",
        json=valid_post,
    )
    print(response.json())
    assert response.status_code == 201
    assert response.json()["img_url"] == "https://www.google.com"
    assert response.json()["img_url_type"] == "absolute"

def test_create_post_invalid_url_type(client: TestClient):
    response = client.post(
        "/post",
        json={
            "img_url": "https://www.google.com",
            "img_url_type": "jpg",
            "caption": "test caption",
            "creator_id": 1,
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] =="Invalid image url type"
  


def test_get_all_posts_success(client: TestClient):
    print(valid_post)
    post =  response = client.post(
        "/post",
        json=valid_post,
    )
    response = client.get("/post/all")
    assert response.status_code == 200
    assert len(response.json()) == 1

# def test_upload_image_success(client: TestClient):
#     response = client.post(
#         "/post/image",
#         files={"image": ("test.jpg", open("tests/test.jpg", "rb"), "image/jpeg")},
#     )
#     assert response.status_code == 200
#     assert response.json()["filename"] == "static/images/test.jpg"