from rest_framework import serializers
from .models import User, Community, Post, Comment, PostVote, CommentVote, Subscription

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'karma', 'avatar_url', 'date_joined']
        read_only_fields = ['id', 'date_joined', 'karma']
        extra_kwargs = {
            'password': {'write_only': True}  # Never return password in response
        }

class CommunitySerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # Allow posting an existing user's PK when auth isn't available yet.
    # Clients can POST {"creator": 1, "name": "...", "description": "..."}
    creator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Community
        fields = ['id', 'creator', 'name', 'description', 'subscriber_count', 'created_at', 'updated_at', 'deleted_at']
        read_only_fields = ['id', 'subscriber_count', 'created_at', 'updated_at', 'deleted_at']


class PostVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVote
        fields = ['id', 'user', 'post', 'vote_value', 'created_at']
        read_only_fields = ['id', 'created_at']


class CommentVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentVote
        fields = ['id', 'user', 'comment', 'vote_value', 'created_at']
        read_only_fields = ['id', 'created_at']


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'community', 'subscribed_at']
        read_only_fields = ['id', 'subscribed_at']


class PostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    community = serializers.PrimaryKeyRelatedField(queryset=Community.objects.all())

    class Meta:
        model = Post
        fields = ['id', 'user', 'community', 'title', 'content', 'post_type', 'vote_count', 'comment_count', 'created_at', 'updated_at', 'deleted_at']
        read_only_fields = ['id', 'vote_count', 'comment_count', 'created_at', 'updated_at', 'deleted_at']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    parent = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'parent', 'content', 'vote_count', 'created_at', 'updated_at', 'deleted_at']
        read_only_fields = ['id', 'vote_count', 'created_at', 'updated_at', 'deleted_at']