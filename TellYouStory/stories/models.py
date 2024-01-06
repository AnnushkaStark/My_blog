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
    is_verificate = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        """
        Отображение полей в админке
        """
        return f"{self.username} {self.email} {self.password}  {self.is_verificate}  {self.is_superuser} {self.is_active}"


class Biography(models.Model):
    """
    Модель биографии пользователя
    заполнение личных данных профиля
    """

    name = models.CharField(max_length=100, blank=True, null=True)
    town = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    avatar = models.ImageField(upload_to="image/avatars/%Y", blank=True, null=True)
    bio = models.TextField(max_length=2000, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        verbose_name_plural = "Biographys"

    def __str__(self):
        return f"{self.name} {self.town} {self.birth_date} {self.link} {self.avatar} {self.bio} {self.user}"
