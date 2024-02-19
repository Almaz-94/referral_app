from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    phone_number = models.IntegerField(unique=True)
    invite_code = models.CharField(max_length=6, unique=True, blank=True, null=True)
    referral_code = models.CharField(max_length=6, unique=True, blank=True, null=True)
    referred_by = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

