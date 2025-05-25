from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth.models import User as AuthUser
from .models import *
from .serializer import *

# AUTHENTICATION
@api_view(['POST'])
@permission_classes([AllowAny])
def auth_register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if AuthUser.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)

    auth_user = AuthUser.objects.create_user(username=username, email=email, password=password)
    print(auth_user)
    return Response({'message': 'Usuário registrado com sucesso'}, status=status.HTTP_201_CREATED)

# USERS
@api_view(['GET'])
def user_index(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def user_create(request):
    serializer = UserSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)