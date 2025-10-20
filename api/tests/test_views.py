import pytest
from rest_framework import status
from api.models import User

@pytest.mark.django_db
class TestUserViewSet:
    
    def test_create_user(self, api_client):
        data = {"username": "NewUser"}
        response = api_client.post("/api/users/", data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1
        assert User.objects.first().username == "NewUser"
    
    def test_list_users(self, api_client, sample_user):
        response = api_client.get("/api/users/")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
    
    def test_retrieve_user(self, api_client, sample_user):
        response = api_client.get(f"/api/users/{sample_user.id}/")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == sample_user.username
    
    def test_update_user(self, api_client, sample_user):
        data = {"username": "UpdatedUser"}
        response = api_client.put(f"/api/users/{sample_user.id}/", data)
        
        assert response.status_code == status.HTTP_200_OK
        sample_user.refresh_from_db()
        assert sample_user.username == "UpdatedUser"
    
    def test_delete_user(self, api_client, sample_user):
        response = api_client.delete(f"/api/users/{sample_user.id}/")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert User.objects.count() == 0