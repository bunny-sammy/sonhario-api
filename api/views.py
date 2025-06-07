from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User
from .models import *
from .serializer import *
from .utils import *

# AUTHENTICATION
@api_view(['POST'])
@permission_classes([AllowAny])
def auth_register_check(request):
    error, status_code = check_register_data(request.data)
    if error:
        return Response(error, status=status_code)

    return Response({'success': True}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def auth_register(request):
    error, status_code = check_register_data(request.data)
    if error:
        return Response(error, status=status_code)
    print("Past user check")
    
    profile_serializer = ProfileSerializer(data = request.data)

    if not profile_serializer.is_valid():
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    new_user = User.objects.create_user(
        username=request.data['username'],
        email=request.data['email'],
        password=request.data['password']
    )

    new_profile = profile_serializer.save(user=new_user)

    return Response({'message': 'Usuário registrado com sucesso!'}, status=status.HTTP_201_CREATED)

# PROFILE
# @api_view(['GET', 'POST'])


# ENTRY
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def entry_index_create(request):
    profile = request.user.profile
    if not profile:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':        
        entries = profile.entries
        serializer = EntrySerializer(entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        serializer = EntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                author=profile,
                age=get_age(profile.birthdate),
                total_sleep_hours=calc_sleep_hours(request.data['sleep_start_time'], request.data['sleep_end_time'])
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def entry_show_update_delete(request, pk):
    try:
        entry = Entry.objects.get(pk=pk)
    except Entry.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = EntrySerializer(entry)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'PUT':
        serializer = EntrySerializer(entry, data=request.data)
        if serializer.is_valid():
            serializer.save(
                total_sleep_hours=calc_sleep_hours(request.data['sleep_start_time'], request.data['sleep_end_time'])
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# USER / PROFILE
@api_view(['GET'])
def user_index(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def user_create(request):
    serializer = ProfileSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    try:
        profile = Profile.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'PUT':
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
