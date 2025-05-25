from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# TEXT CHOICES
class Gender(models.TextChoices):
    MALE = 'Male', 'Male'
    FEMALE = 'Female', 'Female'
    OTHER = 'Other', 'Other'

# MODELS
class Profile (models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile')
    
    display_name = models.CharField(max_length=32)
    birthdate = models.DateField()
    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
        default=Gender.OTHER,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Entry (models.Model):
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='entries'
    )

    date = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
        default=Gender.OTHER,
    )
    sleep_start_time = models.TimeField()
    sleep_end_time = models.TimeField()
    total_sleep_hours = models.FloatField()
    sleep_quality = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    exercise = models.IntegerField()
    caffeine_intake = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.date