from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Модель пользователя"""
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    biography = models.TextField(blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True, upload_to='image/%Y')
    is_superuser = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.username} {self.email} {self.password} {self.biography} {self.avatar} {self.is_superuser}'
    


class Articles(models.Model):
    """
    Модель постов пользователя
    """
    create_date= models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(null=True,blank=True, upload_to='cotent/%Y')
    content = models.TextField(max_length=5000)
    deleted = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.PROTECT)


    def __str__(self):
        return (self.create_date, self.title, self.content, self.image, self.deleted, self.author)

