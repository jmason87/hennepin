from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserList,
    UserDetail,
    CommunityList,
    CommunityDetail,
    PostViewSet,
    CommentList,
    CommentDetail,
    RegisterView,
)

app_name = 'api'

# Router for ViewSets
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('communities/', CommunityList.as_view(), name='community-list'),
    path('communities/<int:pk>/', CommunityDetail.as_view(), name='community-detail'),
    path('comments/', CommentList.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='comment-detail'),
    path("auth/register/", RegisterView.as_view(), name="auth_register"),

    path('', include(router.urls))
]