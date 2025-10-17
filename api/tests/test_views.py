import pytest
from rest_framework import status
from api.models import Item

@pytest.mark.django_db
class TestItemViewSet:
    
    def test_create_item(self, api_client):
        data = {"name": "New Item", "description": "New Description"}
        response = api_client.post("/api/items/", data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Item.objects.count() == 1
        assert Item.objects.first().name == "New Item"
    
    def test_list_items(self, api_client, sample_item):
        response = api_client.get("/api/items/")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
    
    def test_retrieve_item(self, api_client, sample_item):
        response = api_client.get(f"/api/items/{sample_item.id}/")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == sample_item.name
    
    def test_update_item(self, api_client, sample_item):
        data = {"name": "Updated Item", "description": "Updated Description"}
        response = api_client.put(f"/api/items/{sample_item.id}/", data)
        
        assert response.status_code == status.HTTP_200_OK
        sample_item.refresh_from_db()
        assert sample_item.name == "Updated Item"
    
    def test_delete_item(self, api_client, sample_item):
        response = api_client.delete(f"/api/items/{sample_item.id}/")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Item.objects.count() == 0