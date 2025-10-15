from django.urls import path
from .views import ItemListCreate

urlpatterns = [
    path('', ItemListCreate.as_view(), name='item-list-create'),
]