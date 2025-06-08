from rest_framework import serializers
from .models import *
from . import utils

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'display_name', 'birthdate', 'gender']
        extra_kwargs = {
            'user': {'read_only': True}
        }

class EntrySerializer(serializers.ModelSerializer):
    weekday = serializers.SerializerMethodField()
    sleep_hours_string = serializers.SerializerMethodField()
    sleep_hours_short = serializers.SerializerMethodField()

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