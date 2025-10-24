from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    # Don't redefine username, email, password - AbstractUser has them!
    karma = models.IntegerField(default=0)
    avatar_url = models.URLField(blank=True, null=True)
    # created_at is already in AbstractUser as 'date_joined'
    
    def __str__(self):
        return self.username
    
class Community(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='communities'
    )
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    subscriber_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null =True,
        related_name='posts',
    )
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=40000)
    post_type = models.CharField(max_length=100)
    vote_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null =True,
        related_name='comments',
    ) 
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='replies'
    )
    content = models.TextField(max_length=10000)
    vote_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

class PostVote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='post_votes'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='votes'
    )
    vote_value = models.IntegerField()  # e.g. 1 or -1
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_user_post_vote')
        ]

    def __str__(self):
        return f"Vote {self.vote_value} by {self.user_id} on Post {self.post_id}"


class CommentVote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comment_votes'
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='votes'
    )
    vote_value = models.IntegerField()  # e.g. 1 or -1
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'comment'], name='unique_user_comment_vote')
        ]

    def __str__(self):
        return f"Vote {self.vote_value} by {self.user_id} on Comment {self.comment_id}"


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'community'], name='unique_user_community_subscription')
        ]

    def __str__(self):
        return f"{self.user_id} subscribed to {self.community_id}"

