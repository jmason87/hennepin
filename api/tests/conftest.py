import pytest
from rest_framework.test import APIClient
from api.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def sample_user(db):
    user = User.objects.create(username="TestUser")
    user.set_password("password123!")
    user.save()
    return user

@pytest.fixture
def access_token(api_client, sample_user):
    resp = api_client.post(
        "/api/token/",
        {"username": sample_user.username, "password": "password123!"},
        format="json",
    )
    assert resp.status_code == 200, resp.content
    return resp.data["access"]

@pytest.fixture
def auth_client(api_client, access_token):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return api_client