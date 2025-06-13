from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import pandas as pd
# import joblib
from groq import Groq
import os
from . import utils

# model_path = os.path.join(settings.BASE_DIR, 'api', 'ai_agent')
# productivity_model = joblib.load(os.path.join(model_path, 'productivity_model.pkl'))
# stress_model = joblib.load(os.path.join(model_path, 'stress_model.pkl'))

def ask_groq (prompt):
    client = Groq(
        api_key=settings.GROQ_API_KEY,
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content

def sleep_quality (data, age, gender):
    required_fields = ['sleep_start_time', 'sleep_end_time', 'coffee_cups', 'screen_time']
    for field in required_fields:
        if field not in data or not str(data[field]).strip():
            return Response({
                'success': False,
                'error': f'Campo obrigatório: {field}'
            }, status=status.HTTP_400_BAD_REQUEST)

    try:
        coffee_cups = int(data['coffee_cups'])
        screen_time = int(data['screen_time'])
    except ValueError:
        return Response({
            'success': False,
            'error': 'Valores numéricos inválidos'
        }, status=status.HTTP_400_BAD_REQUEST)

    total_sleep_hours = utils.calc_sleep_hours(data['sleep_start_time'], data['sleep_end_time'])
    if total_sleep_hours is None or total_sleep_hours <= 0:
        return Response({
            'success': False,
            'error': 'Combinação de horários inválida'
        }, status=status.HTTP_400_BAD_REQUEST)

    # features = pd.DataFrame([{
    #     'Total Sleep Hours': total_sleep_hours,
    #     'Caffeine Intake (mg)': utils.calc_coffee_cups(coffee_cups),
    #     'Screen Time Before Bed (mins)': screen_time,
    #     'Age': age,
    #     'Gender': gender
    # }])

    try:
        # predicted_productivity = productivity_model.predict(features)[0]
        # predicted_stress = stress_model.predict(features)[0]  

        prompt = f'''
A user has entered the following data for tonight sleep. This app tries to encourage better habits, like avoiding screen time before bed, sleeping an appropriate amount of hours for their age and drinking lower caffeine throught the day. It's important the user understands the importance of their sleeping habits, so really think about the data before responding.
Data = [
'Sleep Start Time': {data['sleep_start_time']},
'Sleep End Time': {data['sleep_end_time']},      
'Total Sleep Hours': {total_sleep_hours}, 
'Caffeine Intake (mg)': {utils.calc_coffee_cups(coffee_cups)} 
'Screen Time Before Bed (mins)': {screen_time},
'Age': {age},
'Gender': {gender}
]
Try and predict, in a scale of 1 to 10:
1) Their productivity score for the next day (1-10)
2) Their stress level for the next day (1-10)
3) A one line of short, concise advice on how to improve their sleep quality based on this data (such as changing sleep times, avoiding screens before bed, drinking less coffee) in imperative but caring language in brazilian portuguese. It's okay to just compliment them if they have healthy habits.
Return ONLY the responses as an int to each of the three points separated by _ with no line breaks, avoiding any extra unnecessary text
                '''
        evaluation = ask_groq(prompt)
        evaluation_data = evaluation.split('_')
        predicted_productivity = evaluation_data[0]
        predicted_stress = evaluation_data[1]

        productivity_string = utils.rating_out_of_ten(predicted_productivity, 'a', True)
        stress_string = utils.rating_out_of_ten(predicted_productivity, 'o', False)

        return Response({
            'success': True,
            'response': evaluation,
            'data': {
                "total_sleep_hours": total_sleep_hours,
                'time_string': utils.time_string(total_sleep_hours),
                "productivity_score": predicted_productivity,
                "productivity_string": productivity_string[0],
                "productivity_color": productivity_string[1],
                "stress_score": predicted_stress,
                "stress_string": stress_string[0],
                "stress_color": stress_string[1],
                'advice': evaluation_data[2]
            },
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': 'Erro interno no processamento',
            'technical': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def weekly_insight (entries, profile):
    print(entries)
    prompt = f'''
A user has entered the following sleep entries in the previous week. This app tries to encourage better habits, like avoiding screen time before bed, sleeping an appropriate amount of hours for their age and drinking lower caffeine throught the day. It's important the user understands the importance of their sleeping habits, so really think about the data before responding.
'''
    for index, entry in enumerate(entries):
        prompt += f'''
Entry {index+1} = [
'Sleep Start Time': {entry.sleep_start_time},
'Sleep End Time': {entry.sleep_end_time},      
'Total Sleep Hours': {entry.total_sleep_hours}, 
'Caffeine Intake (mg)': {entry.caffeine_intake} 
'Screen Time Before Bed (mins)': {entry.screen_time},
'Age': {entry.age},
'Gender': {entry.gender}
]
'''
    prompt += '''
Generate one line of a short, concise review on their latest week of entries and advice on how to improve their sleep quality based on this data (such as changing sleep times, avoiding screens before bed, drinking less coffee) in imperative but caring language in brazilian portuguese. It's okay to just compliment them if they have healthy habits. Avoid stating non integer numbers.
Return ONLY the response avoiding any extra unnecessary text
                '''
    evaluation = ask_groq(prompt)

    return evaluation