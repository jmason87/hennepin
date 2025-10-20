from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Don't redefine username, email, password - AbstractUser has them!
    karma = models.IntegerField(default=0)
    avatar_url = models.URLField(blank=True, null=True)
    # created_at is already in AbstractUser as 'date_joined'
    
    def __str__(self):
        return self.username