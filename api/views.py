from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import pandas as pd
from .models import *
from .serializer import *
from . import utils
from . import insight

# AUTHENTICATION
@api_view(['POST'])
@permission_classes([AllowAny])
def auth_register_check(request):
    error, status_code = utils.check_register_data(request.data)
    if error:
        return Response(error, status=status_code)

    return Response({'message': "Seu nome de usuário e email estão dispníveis"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def auth_register(request):
    error, status_code = utils.check_register_data(request.data)
    if error:
        return Response(error, status=status_code)
    
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
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile_show_update(request):
    profile = request.user.profile
    if not profile:
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

# ENTRY
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def entry_index_create(request):
    profile = request.user.profile
    if not profile:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':        
        entries = profile.entries.order_by('-date')

        paginated = utils.paginate_list(entries, request.query_params)

        serializer = EntrySerializer(paginated, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        serializer = EntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                author=profile,
                age=utils.get_age(profile.birthdate),
                gender=profile.gender,
                caffeine_intake=utils.calc_coffee_cups(request.data['coffee_cups']),
                total_sleep_hours=utils.calc_sleep_hours(request.data['sleep_start_time'], request.data['sleep_end_time'])
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def entry_show_update_delete(request, pk):
    profile = request.user.profile
    if not profile:
        return Response(status=status.HTTP_404_NOT_FOUND)

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
                gender=profile.gender,                
                caffeine_intake=utils.calc_coffee_cups(request.data['coffee_cups']),
                total_sleep_hours=utils.calc_sleep_hours(request.data['sleep_start_time'], request.data['sleep_end_time'])
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# DREAM
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dream_index(request):
    profile = request.user.profile
    if not profile:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    dreams = profile.dreams.order_by('-date')
    paginated = utils.paginate_list(dreams, request.query_params)

    serializer = DreamSerializer(paginated, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def dream_create_show_update_delete (request, pk):
    profile = request.user.profile
    if not profile:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        entry = Entry.objects.get(pk=pk)
    except Entry.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'POST':
        try:
            dream = entry.dream 
            serializer = DreamSerializer(dream, data=request.data)
            if serializer.is_valid():
                serializer.save(
                    entry=entry,
                    date=entry.date
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            serializer = DreamSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(
                    author=profile,
                    entry=entry,
                    date=entry.date
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            dream = entry.dream
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = DreamSerializer(dream)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        if request.method == 'PUT':
            serializer = DreamSerializer(dream, data=request.data)
            if serializer.is_valid():
                serializer.save(
                    entry=entry,
                    date=entry.date
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'DELETE':
            dream.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
# ANÁLISE DE DADOS
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def analyze_entry_quality(request):
    response = insight.sleep_quality(
        request.data,
        utils.get_age(request.user.profile.birthdate),
        request.user.profile.gender
    )
    return response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analyze_weekly_deficit(request):
    profile = request.user.profile
    if not profile:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if profile.entries.count() < 1:
        return Response({"error": "Nenhum registro encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    entries = profile.entries.order_by('-date')[0:6]
    deficit = utils.calc_weekly_deficit(entries, profile)

    return Response(deficit, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analyze_weekly_average(request):
    profile = request.user.profile
    if not profile:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if profile.entries.count() < 1:
        return Response({"error": "Nenhum registro encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    entries = profile.entries.order_by('-date')[0:6]

    average = utils.calc_weekly_average(entries, profile)
    advice = insight.weekly_insight(entries, profile)

    return Response({
        'average': average[0],
        'status': average[1],
        'advice': advice

    }, status=status.HTTP_200_OK)
