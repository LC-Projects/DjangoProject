from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        app_label = 'accounts'
        permissions = [('change_password', 'Can change password')]

    def __str__(self):
        return f'{self.username}'


class Profile(models.Model):
    user = models.OneToOneField(User, null=True , on_delete=models.CASCADE)

    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='images/profiles/', default='https://xsgames.co/randomusers/avatar.php?g=pixel')
    birthdate = models.DateField(null=True, blank=True)
    emotion = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    language = models.CharField(max_length=100, blank=True)

    


    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        # super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user}'