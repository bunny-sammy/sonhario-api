from django.contrib.auth.models import User
from rest_framework import status
from datetime import datetime, timedelta, date

def check_register_data (data):
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return {'error': 'Preencha todos os campos corretamente'}, status.HTTP_400_BAD_REQUEST

    if User.objects.filter(username=username).exists():
        return {'error': 'Este nome de usuário já está em uso'}, status.HTTP_400_BAD_REQUEST

    if User.objects.filter(email=email).exists():
        return {'error': 'Este email já está em uso'}, status.HTTP_400_BAD_REQUEST

    return None, None

def get_age (birthdate):
    today = date.today()
    age = today.year - birthdate.year

    if (today.month, today.day) < (birthdate.month, birthdate.day):
        age -= 1

    print(age)
    return age

def calc_sleep_hours (start_str, end_str, format=True):
    fmt = "%H:%M"
    start = datetime.strptime(start_str, fmt)
    end = datetime.strptime(end_str, fmt)

    if end < start:
        # slept past midnight
        end += timedelta(days=1)

    duration = end - start
    hours = duration.total_seconds() / 3600
    if format: hours = round(hours, 2)

    return hours

def paginate_list (list, queries):
    limit = int(queries.get('limit', 10))
    step = int(queries.get('step', 0))

    start = step * limit
    end = start + limit
    return list[start:end]