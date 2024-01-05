from .models import User
from django import forms
from django.core import validators
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.hashers import make_password, check_password
from django.forms import ModelForm
from django.contrib.auth import authenticate


class UserRegisterForm(ModelForm):
    """
    Обработка формы регитсрации пользователя
    кастомная форма UserCreationForm
    """

    username = forms.CharField(min_length=5, max_length=150, widget=forms.TextInput)
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
        password = self.cleaned_data["password"]
        password2 = self.cleaned_data["password2"]

        if password and password2 and password != password2:
            raise ValidationError("Пароли не совпадают")
        password = make_password(password)
        return password

    class Meta:
        model = User
        fields = ["username", "email", "password"]


class UserLoginForm(forms.Form):
    """
    Форма входа пользователя в систему
    """

    username = forms.CharField(min_length=4, max_length=150, widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)

    def username_clean(self):
        """
        Проверка корректоности  поля username

        """
        username = self.cleaned_data["username"]
        if username:
            return username
        raise ValidationError("InvalidUsername")

    def password_clean(self):
        """
        Проверка корректности поля пароль
        """
        password = self.cleaned_data["password"]
        if password:
            return password
        raise ValidationError("InvalidPassword")


class ChangeMailForm(forms.Form):
    """
    Форма изменения электронной почты пользователя
    """

    old_mail = forms.EmailField(widget=forms.EmailInput)  # Старый адрес эл почты
    new_mail = forms.EmailField(widget=forms.EmailInput)  # Новый адрес эл почты

    def old_mail_clean(self):
        """
        Проверка валидности старой эл почты
        """
        old_mail = self.cleaned_data["old_mail"]
        old = User.objects.filter(email=old_mail)
        if old.count():
            return old_mail
        raise ValidationError("InvalidEmail")

    def new_mail_clean(self):
        """
        Проверка валидности
        новой электронной почты
        """
        new_mail = self.cleaned_data["new_mail"]
        new = User.objects.filter(email=new_mail)
        if new.count():
            raise ValidationError("Почта уже зарегистрировна")
        return new_mail



class ChangePasswordForm(forms.Form):
    """
    Форма изменения пароля пользователя
    """

    old_pass = forms.CharField(widget=forms.PasswordInput)
    new_pass = forms.CharField(widget=forms.PasswordInput)
    new_pass2 = forms.CharField(widget=forms.PasswordInput)

    def old_pass_clean(self):
        """
        Проверка валидности старого пароля
        """
        old_pass = self.cleaned_data["old_pass"]
        if old_pass:
            return old_pass
        raise ValidationError("InvalidPassword")

    def new_pass_clean(self):
        """
        Проверка валидности
        нового пароля
        """
        new_pass = self.cleaned_data["new_pass"]
       
        if new_pass:
            return new_pass
        raise ValidationError("InvalidPassword")
    
    def new_pass_clean(self):
        """
        Проверка валидности
        нового пароля - подтверждения
        """
        new_pass2 = self.cleaned_data["new_pass2"]
       
        if new_pass2:
            return new_pass2
        raise ValidationError("InvalidPassword")
    
    def validate(self):
        """
        Проверка совпадения нового пароля и его подтверждения
        """
        new_pass = self.cleaned_data["new_pass"]
        new_pass2 = self.cleaned_data["new_pass2"]
        if new_pass == new_pass2:
            return new_pass
        return  ValidationError("Пароли не совпадают")
    
      
class DeactivateForm(forms.Form):
    """
    Форма деактивации аккаунта
    """
    username = forms.CharField(min_length=4, max_length=150, widget=forms.TextInput)
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
            return username
        raise ValidationError("Пользователь уже существует")
    
    def email_clean(self):
        """
        Проверка совпадения email
        """
        email = self.cleaned_data["email"]
        new = User.objects.filter(email=email)
        if new.count():
            return email
        raise ValidationError("Неверный адрес электронной почты")

    def clean_password2(self):
        """
        Проверка наличия и совпадения паролей
        """
        password = self.cleaned_data["password"]
        password2 = self.cleaned_data["password2"]

        if password and password2 and password == password2:
            return password
        raise ValidationError("Пароли не совпадают")