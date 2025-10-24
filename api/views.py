from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
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
    error, status_code = utils.check_register_data(request.data, False)
    if error:
        return Response(error, status=status_code)

    return Response({'message': "Seu email está disponível"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def auth_register(request):
    error, status_code = utils.check_register_data(request.data)
    if error:
        return Response(error, status=status_code)
    
    profile_serializer = ProfileSerializer(data = request.data)

    if not profile_serializer.is_valid():
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    new_user = get_user_model().objects.create_user(
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
            new_entry = serializer.save(
                author=profile,
                age=utils.get_age(profile.birthdate),
                gender=profile.gender,
                caffeine_intake=utils.calc_coffee_cups(request.data['coffee_cups']),
                total_sleep_hours=utils.calc_sleep_hours(request.data['sleep_start_time'], request.data['sleep_end_time'])
            )

            try:
                dream_to_link = Dream.objects.get(author=profile, date=new_entry.date)
                dream_to_link.entry = new_entry
                dream_to_link.save()
            except Dream.DoesNotExist:
                pass

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def entry_show_update_delete(request, pk):
    profile = request.user.profile
    if not profile:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        _, entry = utils.get_entry_by_date_or_id(profile, pk)
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
def dream_create_show_update_delete(request, pk):
    profile = request.user.profile
    if not profile:
        return Response(status=status.HTTP_404_NOT_FOUND)

    date, entry_to_save = utils.get_entry_by_date_or_id(profile, pk)
    if not date:
        return Response({"error": "Data inválida"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        dream = Dream.objects.filter(author=profile, date=date).first()
        
        if dream:
            serializer = DreamSerializer(dream, data=request.data)
            status_code = status.HTTP_200_OK
        else:
            serializer = DreamSerializer(data=request.data)
            status_code = status.HTTP_201_CREATED
        
        if serializer.is_valid():
            serializer.save(
                author=profile,
                date=date,
                entry=entry_to_save
            )
            return Response(serializer.data, status=status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
    
    try:
        dream = Dream.objects.get(author=profile, date=date)
    except Dream.DoesNotExist:
        return Response({"error": "No dream found for this date."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DreamSerializer(dream)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'PUT':
        serializer = DreamSerializer(dream, data=request.data)
        if serializer.is_valid():
            serializer.save(
                author=profile,
                date=date,
                entry=entry_to_save
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
    
    entries = profile.entries.order_by('-date')[0:6]
    print(entries)

    deficit = utils.calc_weekly_deficit(entries, profile)

    return Response(deficit, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analyze_weekly_average(request):
    profile = request.user.profile
    if not profile:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    entries = profile.entries.order_by('-date')[0:6]

    average = utils.calc_weekly_average(entries, profile)
    advice = "Sem dados sufricientes para fazer uma análise. Comece a registrar seus hábitos de sono hoje!"
    if (average[0] > 0): advice = insight.weekly_insight(entries, profile)

    return Response({
        'average': average[0],
        'status': average[1],
        'advice': advice

    }, status=status.HTTP_200_OK)
