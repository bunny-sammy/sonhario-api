from rest_framework import serializers
from .models import *
from . import utils

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ['id', 'email', 'password']

    def create(self, validated_data):
        return settings.AUTH_USER_MODEL.objects.create_user(**validated_data)

class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'user', 'first_name', 'display_name', 'age', 'birthdate', 'gender']
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def get_first_name(self, obj):
        return obj.display_name.split(' ')[0]
    
    def get_age(self, obj):
        return utils.get_age(obj.birthdate)

class EntrySerializer(serializers.ModelSerializer):
    weekday = serializers.SerializerMethodField()
    sleep_hours_string = serializers.SerializerMethodField()
    sleep_hours_short = serializers.SerializerMethodField()

    notes = serializers.CharField(
        required=False, 
        allow_null=True,
        style={'base_template': 'textarea.html'}
    )

    class Meta:
        model = Entry
        fields = '__all__'
        read_only_fields = ['age', 'author', 'total_sleep_hours']

    def get_weekday(self, obj):
        return utils.weekdays[obj.date.weekday()]

    def get_sleep_hours_string(self, obj):
        return utils.time_string(obj.total_sleep_hours, False)
    
    def get_sleep_hours_short(self, obj):
        return utils.time_string(obj.total_sleep_hours, True)

class DreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dream
        fields = '__all__'
        read_only_fields = ['author', 'entry', 'date']