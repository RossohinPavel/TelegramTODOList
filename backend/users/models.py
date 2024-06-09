from django.db import models
from django.contrib.auth import models as auth_models
from django.core.validators import RegexValidator


class PhoneValidator(RegexValidator):
    regex = r'8\d{10}'
    message = 'Enter a valid phone number like 89226111020'


# Create your models here.
class User(auth_models.AbstractUser):
    phone = models.CharField(max_length=255, blank=True, null=True, validators=[PhoneValidator()])
