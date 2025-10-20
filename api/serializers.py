from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'karma', 'avatar_url', 'date_joined']
        read_only_fields = ['id', 'date_joined', 'karma']
        extra_kwargs = {
            'password': {'write_only': True}  # Never return password in response
        }