from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class User(AbstractBaseUser):
    '''Модель пользователя'''
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.username} {self.email} {self.password}'