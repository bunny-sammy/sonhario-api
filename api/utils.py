from django.contrib.auth.models import User
from rest_framework import status
from datetime import datetime, timedelta, date

def check_register_data (data):
    # Checa se um usuário existe por username ou email
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
    # Calcula a idade comparando à data atual
    today = date.today()
    age = today.year - birthdate.year

    if (today.month, today.day) < (birthdate.month, birthdate.day):
        age -= 1

    return age

def calc_sleep_hours (start_str, end_str, format=True):
    # Calcula, a partir da hora de início e fim, as horas de sono
    fmt = "%H:%M"
    start = datetime.strptime(start_str, fmt)
    end = datetime.strptime(end_str, fmt)

    if end < start:
        end += timedelta(days=1)

    duration = end - start
    hours = duration.total_seconds() / 3600
    if format: hours = round(hours, 2)

    return hours

def rating_out_of_ten (rating, final_char='o'):
    # Retorna uma string como avaliação
    rating = float(rating)
    if (rating < 4):
        return f"Baix{final_char}"
    elif (rating >= 8):
        return f"Alt{final_char}"
    else:
        return f"Médi{final_char}"
    
def time_string (total_sleep_hours, short=False):
    hours = int(total_sleep_hours)
    minutes = int((total_sleep_hours % 1) * 60)

    if (short):
        if (minutes > 0):
            return f"{hours}h {minutes}m"
        else:
            return f"{hours}h"
    else:        
        if (minutes > 0):
            return f"{hours} horas e {minutes} minutos"
        else:
            return f"{hours} horas"

def calc_coffee_cups (coffee_cups):
    # Retorna a quantidade de miligramas de café baseado no número de copos
    miligrams_per_cup = 95
    return coffee_cups * miligrams_per_cup

def paginate_list (list, queries):
    # Aplica o limite e o step de paginação a uma lista
    limit = int(queries.get('limit', 10))
    step = int(queries.get('step', 0))

    start = step * limit
    end = start + limit
    return list[start:end]

def calc_deficit ():
    # Calcula o deficit de sono
    # A implementar
    return