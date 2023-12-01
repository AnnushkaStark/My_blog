from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Модель пользователя"""
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    biography = models.TextField(blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True, upload_to='image/%Y')

    def __str__(self):
        return f'{self.username} {self.email} {self.password} {self.biography} {self.avatar}'
