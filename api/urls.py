from django.urls import path
from .views import (
    UserList,
    UserDetail,
    CommunityList,
    CommunityDetail,
    PostList,
    PostDetail,
    CommentList,
    CommentDetail,
)

app_name = 'api'

urlpatterns = [
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('communities/', CommunityList.as_view(), name='community-list'),
    path('communities/<int:pk>/', CommunityDetail.as_view(), name='community-detail'),
    path('posts/', PostList.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('comments/', CommentList.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='comment-detail'),
]