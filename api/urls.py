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

'''
ENDPOINTS NECESSÁRIOS

Registro
- Checagem de username e e-mail
- Criação de usuário e perfil

Dashboard (auth)
- Retorna perfil do usuário, as últimas sete entries e o deficit de sono
- Endpoint individual do déficit de sono

Perfil (auth)
- Retorna o perfil do usuário atual
- Atualiza o perfil do usuário atual

Entries (auth)
- Adicionar entry
- Listar entries do usuário
- Listar uma entry por id
- Atualizar entry
- Deletar entry

Dreams (auth)
- Adicionar dream
- Listar dreams do usuário
- Listar uma entry por id
- Atualizar dream
- Deletar dream
'''