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

