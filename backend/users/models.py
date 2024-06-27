from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.
class User(AbstractUser):
    phone = models.CharField(blank=True, validators=(RegexValidator(r'7\d{10}'), ), unique=True)
    telegram_id = models.PositiveIntegerField(blank=True, null=True, unique=True)
