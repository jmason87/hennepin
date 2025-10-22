from django.urls import path
from .views import UserList, UserDetail, CommunityList, CommunityDetail

app_name = 'api'

urlpatterns = [
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('communities/', CommunityList.as_view(), name='community-list'),
    path('communities/<int:pk>/', CommunityDetail.as_view(), name='community-detail'),
]