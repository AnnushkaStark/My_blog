from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    """
    Модель пользователя сайта
    """
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        """
        Отображение полей в админке
        """
        return f'{self.username} {self.email} {self.password}{self.is_superuser} {self.is_active}'