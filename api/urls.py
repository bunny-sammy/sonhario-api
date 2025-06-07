from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views import *

urlpatterns = [
    path('register_check/', auth_register_check, name='register_check'),
    path('register/', auth_register, name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('profile/', profile_show_update, name="profile_show_update"),

    path('entries/', entry_index_create, name="entry_index_create"),
    path('entries/<int:pk>/', entry_show_update_delete, name="entry_show_update_delete"),
    path('entries/dreams/', dream_index, name="dream_index"),
    path('entries/<int:pk>/dream/', dream_create_show_update_delete, name="dream_create_show_update_delete"),
]