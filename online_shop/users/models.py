from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    birthdate = models.DateField(null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True, unique=True, region='RU')
