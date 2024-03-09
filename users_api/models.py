from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Model for custom user with
    'phone_number' as USERNAME_FIELD and
    'authorization_code' as a password
    """
    USERNAME_FIELD = "phone_number"

    username = models.CharField(max_length=30, blank=True, null=True, unique=False)
    phone_number = models.CharField(max_length=13, unique=True)
    authorization_code = models.PositiveSmallIntegerField(blank=True, null=True)
    invite_code = models.CharField(max_length=6, unique=True, blank=True, null=True)
    referral_code = models.CharField(max_length=6, blank=True, null=True)
    referred_by = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"Phone number: {self.phone_number}"

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

