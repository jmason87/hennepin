import pytest
from rest_framework.test import APIClient
from api.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def sample_user(db):
    return User.objects.create(
        username="TestUser",
    )