import pytest
from rest_framework.test import APIClient
from api.models import Item

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def sample_item(db):
    return Item.objects.create(
        name="Test Item",
        description="Test Description"
    )