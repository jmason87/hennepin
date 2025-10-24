import pytest
from rest_framework import status
from api.models import User, Community, Post, Comment

@pytest.mark.django_db
class TestUserViewSet:

    def test_create_user(self, auth_client, sample_user):
        data = {"username": "NewUser"}
        response = auth_client.post("/api/users/", data)

        assert response.status_code == status.HTTP_201_CREATED
        # sample_user already exists + newly created user
        assert User.objects.count() == 2
        assert User.objects.filter(username="NewUser").exists()

    def test_list_users(self, auth_client, sample_user):
        response = auth_client.get("/api/users/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_retrieve_user(self, auth_client, sample_user):
        response = auth_client.get(f"/api/users/{sample_user.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == sample_user.username

    def test_update_user(self, auth_client, sample_user):
        data = {"username": "UpdatedUser"}
        response = auth_client.put(f"/api/users/{sample_user.id}/", data)

        assert response.status_code == status.HTTP_200_OK
        sample_user.refresh_from_db()
        assert sample_user.username == "UpdatedUser"

    def test_delete_user(self, auth_client, sample_user):
        response = auth_client.delete(f"/api/users/{sample_user.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert User.objects.count() == 0


@pytest.mark.django_db
class TestCommunityViewSet:
    def test_create_community(self, auth_client, sample_user):
        data = {"name": "TestCommunity", "description": "A test community"}
        response = auth_client.post("/api/communities/", data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Community.objects.count() == 1
        c = Community.objects.first()
        assert c.name == "TestCommunity"
        assert c.creator_id == sample_user.id

    def test_list_communities(self, auth_client, sample_user):
        Community.objects.create(creator=sample_user, name="ListComm", description="desc")
        response = auth_client.get("/api/communities/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_retrieve_community(self, auth_client, sample_user):
        c = Community.objects.create(creator=sample_user, name="GetComm", description="desc")
        response = auth_client.get(f"/api/communities/{c.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == c.name

    def test_update_community(self, auth_client, sample_user):
        c = Community.objects.create(creator=sample_user, name="OldName", description="old")
        data = {"name": "UpdatedName", "description": "new"}
        response = auth_client.put(f"/api/communities/{c.id}/", data)

        assert response.status_code == status.HTTP_200_OK
        c.refresh_from_db()
        assert c.name == "UpdatedName"

    def test_delete_community(self, auth_client, sample_user):
        c = Community.objects.create(creator=sample_user, name="ToDelete", description="desc")
        response = auth_client.delete(f"/api/communities/{c.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Community.objects.count() == 0


@pytest.mark.django_db
class TestPostViewSet:
    def test_create_post(self, auth_client, sample_user):
        c = Community.objects.create(creator=sample_user, name="PostComm", description="desc")
        data = {"community": c.id, "title": "Hello", "content": "body", "post_type": "text"}
        response = auth_client.post("/api/posts/", data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Post.objects.count() == 1
        p = Post.objects.first()
        assert p.title == "Hello"

    def test_list_posts(self, auth_client, sample_user):
        c = Community.objects.create(creator=sample_user, name="PostComm", description="desc")
        Post.objects.create(user=sample_user, community=c, title="T", content="body", post_type="text")
        response = auth_client.get("/api/posts/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_retrieve_post(self, auth_client, sample_user):
        c = Community.objects.create(creator=sample_user, name="PostComm", description="desc")
        p = Post.objects.create(user=sample_user, community=c, title="T", content="body", post_type="text")
        response = auth_client.get(f"/api/posts/{p.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == p.title

    def test_update_post(self, auth_client, sample_user):
        c = Community.objects.create(creator=sample_user, name="PostComm", description="desc")
        p = Post.objects.create(user=sample_user, community=c, title="Old", content="body", post_type="text")
        data = {"community": c.id, "title": "New", "content": "body", "post_type": "text"}
        response = auth_client.put(f"/api/posts/{p.id}/", data)

        assert response.status_code == status.HTTP_200_OK
        p.refresh_from_db()
        assert p.title == "New"

    def test_delete_post(self, auth_client, sample_user):
        c = Community.objects.create(creator=sample_user, name="PostComm", description="desc")
        p = Post.objects.create(user=sample_user, community=c, title="ToDel", content="body", post_type="text")
        response = auth_client.delete(f"/api/posts/{p.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Post.objects.count() == 0


@pytest.mark.django_db
class TestCommentViewSet:
    def test_create_comment(self, auth_client, sample_user):
        c = Community.objects.create(creator=sample_user, name="ComComm", description="desc")
        p = Post.objects.create(user=sample_user, community=c, title="T", content="body", post_type="text")
        data = {"post": p.id, "content": "hi"}
        response = auth_client.post("/api/comments/", data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Comment.objects.count() == 1

    def test_list_comments(self, auth_client, sample_user):
        c = Community.objects.create(creator=sample_user, name="ComComm", description="desc")
        p = Post.objects.create(user=sample_user, community=c, title="T", content="body", post_type="text")
        Comment.objects.create(user=sample_user, post=p, content="hello")
        response = auth_client.get("/api/comments/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_retrieve_comment(self, auth_client, sample_user):
        c = Community.objects.create(creator=sample_user, name="ComComm", description="desc")
        p = Post.objects.create(user=sample_user, community=c, title="T", content="body", post_type="text")
        com = Comment.objects.create(user=sample_user, post=p, content="hello")
        response = auth_client.get(f"/api/comments/{com.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["content"] == com.content

    def test_update_comment(self, auth_client, sample_user):
        c = Community.objects.create(creator=sample_user, name="ComComm", description="desc")
        p = Post.objects.create(user=sample_user, community=c, title="T", content="body", post_type="text")
        com = Comment.objects.create(user=sample_user, post=p, content="old")
        data = {"post": p.id, "content": "new"}
        response = auth_client.put(f"/api/comments/{com.id}/", data)

        assert response.status_code == status.HTTP_200_OK
        com.refresh_from_db()
        assert com.content == "new"

    def test_delete_comment(self, auth_client, sample_user):
        c = Community.objects.create(creator=sample_user, name="ComComm", description="desc")
        p = Post.objects.create(user=sample_user, community=c, title="T", content="body", post_type="text")
        com = Comment.objects.create(user=sample_user, post=p, content="to del")
        response = auth_client.delete(f"/api/comments/{com.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Comment.objects.count() == 0