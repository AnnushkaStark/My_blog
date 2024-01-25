from .models import User, Biography
from django import forms
from django.core import validators
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.hashers import make_password, check_password
from django.forms import ModelForm
from django.contrib.auth import authenticate
from .validators import valid_name, valid_email, valid_password


class UserRegisterForm(ModelForm):
    """
    Обработка формы регитсрации пользователя
    кастомная форма UserCreationForm
    """

    username = forms.CharField(min_length=3, max_length=50, widget=forms.TextInput)
    email = forms.EmailField(widget=forms.EmailInput,min_length=6, max_length=15)
    password = forms.CharField(widget=forms.PasswordInput,min_length=6, max_length=64)
    password2 = forms.CharField(widget=forms.PasswordInput, min_length=6, max_length=64)

    def username_clean(self):
        """
        Проверка совпадения username
        """
        username = self.cleaned_data["username"]
        if valid_name("username") == "is_valid":
            new = User.objects.filter(username=username)
            if new.count():
                raise ValidationError("Пользователь уже существует")
            return username
        raise ValidationError(
            "Длина имени пользователя должна быть от 3х до 50 символов"
        )

    def email_clean(self):
        """
        Проверка совпадения email
        """
        email = self.cleaned_data["email"]
        if valid_email(email) == "is_valid":
            email = self.cleaned_data["email"]
            new = User.objects.filter(email=email)
            if new.count():
                raise ValidationError("Почта уже зарегистрировна")
            return email
        raise ValidationError("Почта уже зарегистрировна")
    
    def clean_password2(self):
        """
        Проверка наличия и совпадения паролей
        """
        password = self.cleaned_data["password"]
        if valid_password(password) == "is_valid":
            password2 = self.cleaned_data["password2"]

            if password and password2 and password != password2:
                raise ValidationError("Пароли не совпадают")
            password = make_password(password)
            return password
        raise forms.ValidationError("Пароль слишком простой")
    
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
        return ValidationError("Пароли не совпадают")


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


class NameChangeForm(forms.Form):
    """
    Форма изменения имени пользователя
    """

    name = forms.CharField(required=False, max_length=100, widget=forms.TextInput)

    def name_clean(self):
        """
        получение имени пользователя
        """
        name = self.cleaned_data["name"]

        return name


class ChangeTownForm(forms.Form):
    """
    Форма изменения города пользователя
    """

    town = forms.CharField(required=False, max_length=100, widget=forms.TextInput)

    def town_clean(self):
        """
        получение города пользователя пользователя
        """
        town = self.cleaned_data["town"]

        return town


class BirthDateForm(forms.Form):
    """
    Форма изменения даты рождения
    пользователя
    """

    birth_date = forms.DateField(required=False, widget=forms.DateInput)

    def date_clean(self):
        """
        получение даты рождения пользователя
        """
        birth_date = self.cleaned_data["birth_date"]

        return birth_date


class FormLinkChange(forms.Form):
    """
    Изменение ссылки на соц сеть или бусти
    в профиле пользователя
    """

    link = forms.URLField(required=False, widget=forms.URLInput)

    def link_clean(self):
        """
        получение ссылки на соцсеть или бусти пользователя
        """
        link = self.cleaned_data["link"]

        return link


class AvatarChangeForm(forms.Form):
    """
    Форма изменения аватакри профиля
    """

    avatar = forms.FileField(required=False, widget=forms.FileInput)

    def avatar_clean(self):
        """
        получение фото профиля пользователя
        """
        avatar = self.cleaned_data["avatar"]

        return avatar


class BioChangeForm(forms.Form):
    """
    Форма изменения биографии пользователя
    """

    bio = forms.Textarea()

    def bio_clean(self):
        """
        получение биографии пользователя
        """
        bio = self.data["bio"]

        return bio
