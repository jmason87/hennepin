from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import User, Community
from .serializers import UserSerializer, CommunitySerializer

class UserList(generics.ListCreateAPIView):
    """List all Users or create a new User."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]  # Add later when auth is ready

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a User."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]  # Add later

class CommunityList(generics.ListCreateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

class CommunityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer