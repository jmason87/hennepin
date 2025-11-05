import pytest
from rest_framework import status
from api.models import User, Community, Post, Comment, PostVote, Subscription

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

    def test_subscribe_to_community(self, auth_client, sample_user):
        """Test subscribing to a community"""
        c = Community.objects.create(creator=sample_user, name="SubComm", description="desc")
        
        response = auth_client.post(f"/api/communities/{c.id}/subscribe/")
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["message"] == "Subscribed"
        assert response.data["subscriber_count"] == 1
        assert response.data["is_subscribed"] is True
        
        c.refresh_from_db()
        assert c.subscriber_count == 1
        assert Subscription.objects.filter(user=sample_user, community=c).exists()

    def test_subscribe_already_subscribed(self, auth_client, sample_user):
        """Test subscribing when already subscribed"""
        c = Community.objects.create(creator=sample_user, name="SubComm", description="desc")
        Subscription.objects.create(user=sample_user, community=c)
        c.subscriber_count = 1
        c.save()
        
        response = auth_client.post(f"/api/communities/{c.id}/subscribe/")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Already subscribed"
        assert response.data["is_subscribed"] is True

    def test_unsubscribe_from_community(self, auth_client, sample_user):
        """Test unsubscribing from a community"""
        c = Community.objects.create(creator=sample_user, name="UnsubComm", description="desc")
        Subscription.objects.create(user=sample_user, community=c)
        c.subscriber_count = 1
        c.save()
        
        response = auth_client.delete(f"/api/communities/{c.id}/unsubscribe/")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Unsubscribed"
        assert response.data["subscriber_count"] == 0
        assert response.data["is_subscribed"] is False
        
        c.refresh_from_db()
        assert c.subscriber_count == 0
        assert not Subscription.objects.filter(user=sample_user, community=c).exists()

    def test_unsubscribe_not_subscribed(self, auth_client, sample_user):
        """Test unsubscribing when not subscribed"""
        c = Community.objects.create(creator=sample_user, name="UnsubComm", description="desc")
        
        response = auth_client.delete(f"/api/communities/{c.id}/unsubscribe/")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "error" in response.data

    def test_is_subscribed_field_in_serializer(self, auth_client, sample_user):
        """Test that is_subscribed field shows subscription status"""
        c = Community.objects.create(creator=sample_user, name="SubComm", description="desc")
        
        # Not subscribed
        response = auth_client.get(f"/api/communities/{c.id}/")
        assert response.data["is_subscribed"] is False
        
        # After subscribing
        Subscription.objects.create(user=sample_user, community=c)
        response = auth_client.get(f"/api/communities/{c.id}/")
        assert response.data["is_subscribed"] is True


@pytest.mark.django_db
class TestPostViewSet:
    def test_create_post(self, auth_client, sample_user):
        c = Community.objects.create(creator=sample_user, name="PostComm", description="desc")
        data = {"community_id": c.id, "title": "Hello", "content": "body", "post_type": "text"}
        response = auth_client.post("/api/posts/", data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Post.objects.count() == 1
        p = Post.objects.first()
        assert p.title == "Hello"
        # Verify nested serialization
        assert "user" in response.data
        assert "username" in response.data["user"]
        assert response.data["user"]["username"] == sample_user.username
        assert "community" in response.data
        assert "name" in response.data["community"]
        assert response.data["community"]["name"] == c.name

    def test_list_posts(self, auth_client, sample_user):
        c = Community.objects.create(creator=sample_user, name="PostComm", description="desc")
        Post.objects.create(user=sample_user, community=c, title="T", content="body", post_type="text")
        response = auth_client.get("/api/posts/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        # Verify nested serialization in list view
        assert "user" in response.data[0]
        assert "username" in response.data[0]["user"]
        assert "community" in response.data[0]
        assert "name" in response.data[0]["community"]

    def test_retrieve_post(self, auth_client, sample_user):
        c = Community.objects.create(creator=sample_user, name="PostComm", description="desc")
        p = Post.objects.create(user=sample_user, community=c, title="T", content="body", post_type="text")
        response = auth_client.get(f"/api/posts/{p.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == p.title
        # Verify nested serialization
        assert isinstance(response.data["user"], dict)
        assert isinstance(response.data["community"], dict)

    def test_update_post(self, auth_client, sample_user):
        c = Community.objects.create(creator=sample_user, name="PostComm", description="desc")
        p = Post.objects.create(user=sample_user, community=c, title="Old", content="body", post_type="text")
        data = {"title": "New", "content": "body", "post_type": "text"}
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

    def test_get_post_comments(self, auth_client, sample_user):
        """Test getting comments for a specific post"""
        c = Community.objects.create(creator=sample_user, name="PostComm", description="desc")
        p = Post.objects.create(user=sample_user, community=c, title="Test", content="body", post_type="text")
        
        # Create some comments
        Comment.objects.create(user=sample_user, post=p, content="First comment")
        Comment.objects.create(user=sample_user, post=p, content="Second comment")
        
        # Create comment on different post (should not appear)
        p2 = Post.objects.create(user=sample_user, community=c, title="Other", content="body", post_type="text")
        Comment.objects.create(user=sample_user, post=p2, content="Other comment")
        
        response = auth_client.get(f"/api/posts/{p.id}/comments/")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]["content"] == "First comment"
        assert response.data[1]["content"] == "Second comment"


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


@pytest.mark.django_db
class TestRegistration:
    def test_register_success_returns_tokens(self, api_client):
        payload = {
            "username": "alice",
            "email": "alice@example.com",
            "password": "Str0ng!Pass123",
            "password2": "Str0ng!Pass123",
        }
        resp = api_client.post("/api/auth/register/", payload, format="json")

        assert resp.status_code == status.HTTP_201_CREATED, resp.content
        data = resp.data
        # response shape
        assert "user" in data and "access" in data and "refresh" in data
        assert data["user"]["username"] == "alice"
        # user actually exists
        assert User.objects.filter(username="alice").exists()

    def test_register_mismatched_passwords(self, api_client):
        payload = {
            "username": "bob",
            "email": "bob@example.com",
            "password": "Str0ng!Pass123",
            "password2": "Different!Pass123",
        }
        resp = api_client.post("/api/auth/register/", payload, format="json")

        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "password2" in resp.data


@pytest.mark.django_db
class TestPostVoting:
    def test_upvote_post(self, auth_client, sample_user):
        """Test creating an upvote on a post"""
        community = Community.objects.create(creator=sample_user, name="TestComm", description="desc")
        post = Post.objects.create(user=sample_user, community=community, title="Test", content="body", post_type="text")
        
        response = auth_client.post(f"/api/posts/{post.id}/vote/", {"vote_value": 1}, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED, response.data
        assert response.data["message"] == "Vote created"
        assert response.data["vote_count"] == 1
        assert response.data["user_vote"] == 1
        
        post.refresh_from_db()
        assert post.vote_count == 1
        assert PostVote.objects.filter(user=sample_user, post=post, vote_value=1).exists()

    def test_downvote_post(self, auth_client, sample_user):
        """Test creating a downvote on a post"""
        community = Community.objects.create(creator=sample_user, name="TestComm", description="desc")
        post = Post.objects.create(user=sample_user, community=community, title="Test", content="body", post_type="text")
        
        response = auth_client.post(f"/api/posts/{post.id}/vote/", {"vote_value": -1}, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["vote_count"] == -1
        assert response.data["user_vote"] == -1
        
        post.refresh_from_db()
        assert post.vote_count == -1

    def test_toggle_vote_removes_it(self, auth_client, sample_user):
        """Test clicking same vote again removes it"""
        community = Community.objects.create(creator=sample_user, name="TestComm", description="desc")
        post = Post.objects.create(user=sample_user, community=community, title="Test", content="body", post_type="text")
        
        # First vote
        auth_client.post(f"/api/posts/{post.id}/vote/", {"vote_value": 1}, format='json')
        
        # Toggle off
        response = auth_client.post(f"/api/posts/{post.id}/vote/", {"vote_value": 1}, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Vote removed"
        assert response.data["vote_count"] == 0
        assert response.data["user_vote"] is None
        
        post.refresh_from_db()
        assert post.vote_count == 0
        assert not PostVote.objects.filter(user=sample_user, post=post).exists()

    def test_switch_vote_from_up_to_down(self, auth_client, sample_user):
        """Test switching from upvote to downvote"""
        community = Community.objects.create(creator=sample_user, name="TestComm", description="desc")
        post = Post.objects.create(user=sample_user, community=community, title="Test", content="body", post_type="text")
        
        # Upvote
        auth_client.post(f"/api/posts/{post.id}/vote/", {"vote_value": 1}, format='json')
        
        # Switch to downvote
        response = auth_client.post(f"/api/posts/{post.id}/vote/", {"vote_value": -1}, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Vote updated"
        assert response.data["vote_count"] == -1
        assert response.data["user_vote"] == -1
        
        post.refresh_from_db()
        assert post.vote_count == -1
        assert PostVote.objects.filter(user=sample_user, post=post, vote_value=-1).exists()

    def test_switch_vote_from_down_to_up(self, auth_client, sample_user):
        """Test switching from downvote to upvote"""
        community = Community.objects.create(creator=sample_user, name="TestComm", description="desc")
        post = Post.objects.create(user=sample_user, community=community, title="Test", content="body", post_type="text")
        
        # Downvote
        auth_client.post(f"/api/posts/{post.id}/vote/", {"vote_value": -1}, format='json')
        
        # Switch to upvote
        response = auth_client.post(f"/api/posts/{post.id}/vote/", {"vote_value": 1}, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Vote updated"
        assert response.data["vote_count"] == 1
        assert response.data["user_vote"] == 1
        
        post.refresh_from_db()
        assert post.vote_count == 1

    def test_delete_vote(self, auth_client, sample_user):
        """Test DELETE request removes vote"""
        community = Community.objects.create(creator=sample_user, name="TestComm", description="desc")
        post = Post.objects.create(user=sample_user, community=community, title="Test", content="body", post_type="text")
        
        # Create vote
        auth_client.post(f"/api/posts/{post.id}/vote/", {"vote_value": 1}, format='json')
        
        # Delete vote
        response = auth_client.delete(f"/api/posts/{post.id}/vote/")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Vote removed"
        assert response.data["vote_count"] == 0
        assert response.data["user_vote"] is None
        
        post.refresh_from_db()
        assert post.vote_count == 0
        assert not PostVote.objects.filter(user=sample_user, post=post).exists()

    def test_delete_nonexistent_vote_returns_404(self, auth_client, sample_user):
        """Test deleting a vote that doesn't exist"""
        community = Community.objects.create(creator=sample_user, name="TestComm", description="desc")
        post = Post.objects.create(user=sample_user, community=community, title="Test", content="body", post_type="text")
        
        response = auth_client.delete(f"/api/posts/{post.id}/vote/")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "error" in response.data

    def test_invalid_vote_value_returns_400(self, auth_client, sample_user):
        """Test invalid vote values are rejected"""
        community = Community.objects.create(creator=sample_user, name="TestComm", description="desc")
        post = Post.objects.create(user=sample_user, community=community, title="Test", content="body", post_type="text")
        
        # Test various invalid values
        for invalid_value in [0, 2, -2, "up"]:
            response = auth_client.post(f"/api/posts/{post.id}/vote/", {"vote_value": invalid_value}, format='json')
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert "error" in response.data

    def test_concurrent_votes_dont_lose_count(self, auth_client, sample_user):
        """Test that F() expressions prevent race conditions"""
        community = Community.objects.create(creator=sample_user, name="TestComm", description="desc")
        post = Post.objects.create(user=sample_user, community=community, title="Test", content="body", post_type="text")
        
        # Create another user
        user2 = User.objects.create_user(username="user2", password="pass")
        
        # Both users upvote
        auth_client.post(f"/api/posts/{post.id}/vote/", {"vote_value": 1}, format='json')
        
        # Authenticate as second user
        auth_client.force_authenticate(user=user2)
        auth_client.post(f"/api/posts/{post.id}/vote/", {"vote_value": 1}, format='json')
        
        post.refresh_from_db()
        assert post.vote_count == 2
        assert PostVote.objects.filter(post=post).count() == 2

    def test_user_vote_field_in_serializer(self, auth_client, sample_user):
        """Test that user_vote field shows current user's vote"""
        community = Community.objects.create(creator=sample_user, name="TestComm", description="desc")
        post = Post.objects.create(user=sample_user, community=community, title="Test", content="body", post_type="text")
        
        # No vote yet
        response = auth_client.get(f"/api/posts/{post.id}/")
        assert response.data["user_vote"] is None
        
        # After upvoting
        auth_client.post(f"/api/posts/{post.id}/vote/", {"vote_value": 1}, format='json')
        response = auth_client.get(f"/api/posts/{post.id}/")
        assert response.data["user_vote"] == 1
        
        # After downvoting
        auth_client.post(f"/api/posts/{post.id}/vote/", {"vote_value": -1}, format='json')
        response = auth_client.get(f"/api/posts/{post.id}/")
        assert response.data["user_vote"] == -1