from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    birthdate = models.DateField(
        'День рождения',
        null=True,
        blank=True)
    phone_number = PhoneNumberField(
        'Номер телефона',
        help_text='Укажите ваш номер телефона',
        null=True,
        blank=True,
        unique=True,
        region='RU')
    favorites = models.ManyToManyField(
        'store.Product',
        related_name='favorited_by')
