from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        app_label = 'accounts'
        permissions = [('change_password', 'Can change password')]

    def __str__(self):
        return f'{self.username}'