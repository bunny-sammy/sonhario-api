from django.urls import path
from .views import *

urlpatterns = [
    path('users/', user_index, name="user_index"),
    path('users/create', user_create, name="user_create"),
    path('users/<int:pk>', user_detail, name="user_detail"),
]