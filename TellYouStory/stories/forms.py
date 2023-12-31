from .models import User
from django import forms
from django.core import validators
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password


class UserRegisterForm(UserCreationForm):
    """
    Обработка формы регитсрации пользователя
    кастомная форма UserCreationForm
    """

    username = forms.CharField(min_length=5, max_length=150)
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def username_clean(self):
        """
        Проверка совпадения username
        """
        username = self.cleaned_data["username"]
        new = User.objects.filter(username=username)
        if new.count():
            raise ValidationError("Пользователь уже существует")
        return username

    def email_clean(self):
        """
        Проверка совпадения email
        """
        email = self.cleaned_data["email"]
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError("Почта уже зарегистрировна")
        return email

    def clean_password2(self):
        """
        Проверка наличия и совпадения паролей
        """
        password = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]

        if password and password2 and password != password2:
            raise ValidationError("Пароли не совпадают")
        password = make_password(password)
        return password

    def save(self, commit=True):
        """
        Создание объекта пользователя
        """
        user = User.objects.create(
            self.cleaned_data["username"],
            self.cleaned_data["email"],
            self.cleaned_data["password1"],
        )
        return user
