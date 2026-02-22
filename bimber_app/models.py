from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    class Gender(models.TextChoices):
        MALE = 'M'
        FEMALE = 'F'
    age = models.IntegerField(null=False, blank=False)
    gender = models.CharField(choices=Gender.choices)
    bio = models.TextField(null=False, blank=False)
    score = models.IntegerField(null=False, default=500)
    city = models.CharField(null=False, blank=False)
    photo = models.ImageField(upload_to="user/photos", blank=True, null=True)
