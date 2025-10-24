from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

# TEXT CHOICES
class Gender(models.TextChoices):
    MALE = 'Male', 'Male'
    FEMALE = 'Female', 'Female'
    OTHER = 'Other', 'Other'

class Emotions(models.IntegerChoices):
    HAPPY = 1, 'Happy'
    SAD = 2, 'Sad'
    NEUTRAL = 3, 'Neutral'

# MODELS
class Profile (models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
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
        null=True, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    exercise = models.IntegerField(null=True)
    caffeine_intake = models.IntegerField(null=True)
    screen_time = models.IntegerField(null=True)
    work_hours = models.FloatField(null=True)
    productivity_score = models.IntegerField(
        null=True, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    mood_score = models.IntegerField(
        null=True, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    stress_level = models.IntegerField(
        null=True, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    notes = models.TextField(
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.date.strftime("%Y-%m-%d")
    
class Dream (models.Model):
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='dreams'
    )
    entry = models.OneToOneField(
        Entry,
        null=True,
        on_delete=models.CASCADE,
        related_name='dream'
    )
    emotion = models.IntegerField(
        choices=Emotions.choices,
        default=Emotions.NEUTRAL,
    )

    date = models.DateField()
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.date.strftime("%Y-%m-%d")