from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from django.db.models import F
from .models import User, Community, Post, Comment, PostVote
from .serializers import (
    UserSerializer,
    CommunitySerializer,
    PostSerializer,
    CommentSerializer,
    RegistrationSerializer,
)

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        data = {
            "user": UserSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

class CommunityList(generics.ListCreateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticated]

class CommunityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticated]

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post', 'delete'])
    def vote(self, request, pk=None):
        post = self.get_object()
        existing_vote = PostVote.objects.filter(user=request.user, post=post).first()
        
        if request.method == 'POST':
            vote_value = request.data.get('vote_value')
            if vote_value not in [1, -1]:
                return Response(
                    {'error': 'vote_value must be 1 or -1'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if existing_vote:
                if existing_vote.vote_value == vote_value:
                    # Toggle off - remove vote
                    delta = -existing_vote.vote_value
                    existing_vote.delete()
                    user_vote = None
                    message = 'Vote removed'
                    response_status = status.HTTP_200_OK
                else:
                    # Switch vote
                    delta = vote_value - existing_vote.vote_value
                    existing_vote.vote_value = vote_value
                    existing_vote.save()
                    user_vote = vote_value
                    message = 'Vote updated'
                    response_status = status.HTTP_200_OK
            else:
                # New vote
                PostVote.objects.create(user=request.user, post=post, vote_value=vote_value)
                delta = vote_value
                user_vote = vote_value
                message = 'Vote created'
                response_status = status.HTTP_201_CREATED
            
            post.vote_count = F('vote_count') + delta
            post.save(update_fields=['vote_count'])
            post.refresh_from_db()
            
            return Response({
                'message': message,
                'vote_count': post.vote_count,
                'user_vote': user_vote
            }, status=response_status)
            
        else:  # DELETE
            if not existing_vote:
                return Response(
                    {'error': 'No vote to remove'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            post.vote_count = F('vote_count') - existing_vote.vote_value
            existing_vote.delete()
            post.save(update_fields=['vote_count'])
            post.refresh_from_db()
            
            return Response({
                'message': 'Vote removed',
                'vote_count': post.vote_count,
                'user_vote': None
            })

class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]