from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserList,
    UserDetail,
    CommunityViewSet,
    PostViewSet,
    CommentList,
    CommentDetail,
    RegisterView,
)

app_name = 'api'

# Router for ViewSets
router = DefaultRouter()
router.register(r'communities', CommunityViewSet, basename='community')
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('comments/', CommentList.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='comment-detail'),
    path("auth/register/", RegisterView.as_view(), name="auth_register"),

    path('', include(router.urls))
]