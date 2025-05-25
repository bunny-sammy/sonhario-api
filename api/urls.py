from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views import *

urlpatterns = [
    path('register/', auth_register, name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('users/', user_index, name="user_index"),
    path('users/create', user_create, name="user_create"),
    path('users/<int:pk>', user_detail, name="user_detail"),
]