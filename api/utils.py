from django.contrib.auth import get_user_model
from rest_framework import status
from datetime import datetime, timedelta, date, time

weekdays = {
    0: 'Seg',
    1: 'Ter',
    2: 'Qua',
    3: 'Qui',
    4: 'Sex',
    5: 'Sáb',
    6: 'Dom'
}

def check_register_data(data, login=True):
    # Checa se os dados de registro são válidos para o CustomUser model.
    # Verifica se o email já está em uso.
    User = get_user_model()

    email = data.get('email')
    password = data.get('password')

    if not email or (login and not password):
        return {'error': 'Todos os campos precisam ser preenchidos'}, status.HTTP_400_BAD_REQUEST

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

def parse_time(value):
    if isinstance(value, time):
        return value
    if isinstance(value, datetime):
        return value.time()
    if isinstance(value, str):
        return datetime.strptime(value, "%H:%M").time()
    raise ValueError("Unsupported time format")

def calc_sleep_hours (start_str, end_str, format=True):
    # Calcula, a partir da hora de início e fim, as horas de sono
    fmt = "%H:%M"
    start = parse_time(start_str)
    end = parse_time(end_str)

    today = datetime.today().date()
    start_dt = datetime.combine(today, start)
    end_dt = datetime.combine(today, end)

    if end_dt < start_dt:
        end_dt += timedelta(days=1)

    duration = end_dt - start_dt
    hours = duration.total_seconds() / 3600
    if format: hours = round(hours, 2)

    return hours

def rating_out_of_ten (rating, final_char='o', good=True):
    # Retorna uma string como avaliação
    rating = float(rating)
    if (rating < 4):
        return f"Baix{final_char}", 3 if good else 1
    elif (rating >= 8):
        return f"Alt{final_char}", 1 if good else 3
    else:
        return f"Médi{final_char}", 2
    
def time_string (time, short=False):
    hours = int(time)
    minutes = int((time % 1) * 60)

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

def sleep_requirement_by_age (age):
    # Calcula o mínimo de horas de sono por noite baseado na idade do indivíduo
    requirement = 8
    if (age <= 18): requirement += 1
    if (age <= 12): requirement += 1

    return requirement

def calc_weekly_deficit (entries, author):
    # Calcula o deficit de sono da última semana
    requirement = sleep_requirement_by_age(get_age(author.birthdate))
    deficit = 0

    for entry in entries:
        sleep_hours = calc_sleep_hours(entry.sleep_start_time, entry.sleep_end_time)
        daily_deficit = requirement - sleep_hours
        deficit += daily_deficit

    status = "even"
    if deficit > 0:
        status = "deficit"
    if deficit < 0:
        status = "surplus"

    return {"status": status, "value": abs(round(deficit))}

def calc_weekly_average (entries, author):
    # Calcula a média de horas dormidas por noite na última semana
    requirement = sleep_requirement_by_age(get_age(author.birthdate))
    wiggle_room = 2
    times_total = 0
    count = 0

    for entry in entries:
        sleep_hours = calc_sleep_hours(entry.sleep_start_time, entry.sleep_end_time)
        times_total += sleep_hours
        count += 1

    if (count == 0): count += 1

    average = times_total / count
    average = round(average)
    verdict = "Dentro do recomendado"
    if average > requirement + wiggle_room:
        verdict = "Acima da média"
    if average < requirement - wiggle_room:
        verdict = "Abaixo do ideal"

    return average, verdict