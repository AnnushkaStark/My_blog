from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import User, Story, FeedBackUsers, FeedBackPublic, Report
from .validators import (
    valid_name,
    valid_email,
    valid_password,
    valid_text,
    valid_image
)


class UserRegisterForm(ModelForm):
    """
    Обработка формы регитсрации пользователя
    кастомная форма UserCreationForm
    """

    username = forms.CharField(
        min_length=3, max_length=50, widget=forms.TextInput
    )
    email = forms.EmailField(
        widget=forms.EmailInput, min_length=6, max_length=25
    )
    password = forms.CharField(
        widget=forms.PasswordInput, min_length=6, max_length=64
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput, min_length=6, max_length=64
    )

    def clean(self):
        """
        Валидация данных
        """
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if username and email and password and password2:
            if (
                valid_name("username") == "is_valid"
                and valid_text("username") == "is_valid"
            ):
                if User.objects.filter(username=username).count() == 0:
                    if valid_email(email) == "is_valid":
                        if User.objects.filter(email=email).count() == 0:
                            if (
                                valid_password(password) == "is_valid"
                                and valid_password(password2) == "is_valid"
                            ):
                                if password == password2:
                                    return cleaned_data
                                raise ValidationError("Пароли не совпадают")
                            raise forms.ValidationError("Пароль слишком простой")
                        raise ValidationError("Почта уже зарегистрировна")
                    raise ValidationError("Ведите корректную электронную почту")
                raise ValidationError("Пользователь уже существует")
            raise ValidationError("Некорректное имя пользователя")
        raise ValidationError("Поле не может быть путсым")

    class Meta:
        model = User
        fields = ["username", "email", "password"]


class UserLoginForm(forms.Form):
    """
    Форма входа пользователя в систему
    """

    username = forms.CharField(
        min_length=4, max_length=150, widget=forms.TextInput
    )
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

    old_mail = forms.EmailField(
        widget=forms.EmailInput, min_length=6, max_length=25
    )  # Старый адрес эл почты
    new_mail = forms.EmailField(
        widget=forms.EmailInput, min_length=6, max_length=25
    )

    def clean(self):
        """
        Валидация данных
        """
        cleaned_data = super().clean()
        old_mail = cleaned_data.get("old_mail")
        new_mail = cleaned_data.get("new_mail")

        if old_mail and new_mail:
            if valid_email(old_mail) == "is_valid":
                if valid_email(new_mail) == "is_valid":
                    if User.objects.filter(email=new_mail).count() == 0:
                        return cleaned_data
                    raise forms.ValidationError(f"Почта {new_mail} уже зарегистрировна")
                raise forms.ValidationError(f"Введите корректный email")
            raise forms.ValidationError(f"Введите корректный email")
        raise forms.ValidationError(f"Поле не может быть пустым")


class ChangePasswordForm(forms.Form):
    """
    Форма изменения пароля пользователя
    """

    old_pass = forms.CharField(
        widget=forms.PasswordInput, min_length=6, max_length=64
    )
    new_pass = forms.CharField(
        widget=forms.PasswordInput, min_length=6, max_length=64
    )
    new_pass2 = forms.CharField(
        widget=forms.PasswordInput, min_length=6, max_length=64
    )

    def clean(self):
        """
        Валидация  формы
        """
        cleaned_data = super().clean()
        old_pass = cleaned_data.get("old_pass")
        new_pass = cleaned_data.get("new_pass")
        new_pass2 = cleaned_data.get("new_pass2")

        if old_pass and new_pass and new_pass2:
            if new_pass2 == new_pass:
                if valid_password(new_pass) == "is_valid":
                    return cleaned_data
                raise forms.ValidationError("Пароль слишком простой")
            raise forms.ValidationError("Пароли не совпадают")
        raise forms.ValidationError("Поле не может быть пустым")


class DeactivateForm(forms.Form):
    """
    Форма деактивации аккаунта
    """

    username = forms.CharField(
        min_length=4, max_length=150, widget=forms.TextInput
    )
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

    name = forms.CharField(
        required=False, max_length=100, widget=forms.TextInput
    )

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

    town = forms.CharField(
        required=False, max_length=100, widget=forms.TextInput
    )

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

    def clean(self):
        """
        получение фото профиля пользователя
        """
        cleaned_data = super().clean()
        avatar = self.cleaned_data.get("avatar")
        try:
            if valid_image(avatar) == "is_valid":
                return cleaned_data
            raise forms.ValidationError("Некорректное разрешение файла")
        except AttributeError:
            return cleaned_data


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


class AddArticleForm(ModelForm):
    """
    Форма добавления статьи
    """

    title = forms.CharField(
        min_length=3, max_length=100, widget=forms.TextInput
    )
    topic = forms.CharField(
        min_length=3, max_length=100, widget=forms.TextInput
    )
    image = forms.FileField(required=False, widget=forms.FileInput)
    content = forms.Textarea()

    def clean(self):
        """
        Валидация  формы
        """
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        topic = cleaned_data.get("topic")
        image = cleaned_data.get("image")
        content = cleaned_data.get("content")

        if (title and topic and image) or (title and topic and content):
            try:
                if (
                    valid_text(title) == "is_valid"
                    and valid_text(topic) == "is_valid"
                    and valid_text(content) == "is_valid"
                    and valid_image(image) == "is_valid"
                ):
                    return cleaned_data
                raise forms.ValidationError("Контент не проходит цензуру")
            except AttributeError:
                return cleaned_data
        raise forms.ValidationError(
            "Поле изображение или поле контент должно быть заполнено"
        )

    class Meta:
        model = Story
        fields = ["title", "topic", "image", "content"]


class FeedBackUserForm(forms.ModelForm):
    """
    Форма писем обратной ствязи от
    аутентифицированных пользователей
    """

    topic = forms.CharField(
        widget=forms.TextInput, min_length=3, max_length=150
    )
    description = forms.Textarea()

    def clean(self):
        """
        Валидация данных
        """
        cleaned_data = super().clean()
        topic = cleaned_data.get("topic")
        description = cleaned_data.get("description")
        if topic and description:
            if (
                valid_text(topic) == "is_valid"
                and valid_text(description) == "is_valid"
            ):
                return cleaned_data
            raise forms.ValidationError("Данные не прошли модерацию")
        raise forms.ValidationError("Поля не могут быть пустыми")

    class Meta:
        model = FeedBackUsers
        fields = [
            "topic",
            "description",
        ]


class FeedbackPublicForm(forms.ModelForm):
    """
    Форма отправления обратной связи
    для не аутентифицированного пользователя
    """

    name = forms.CharField(widget=forms.TextInput, min_length=3, max_length=50)
    email = forms.EmailField(
        widget=forms.EmailInput, min_length=6, max_length=20
    )
    topic = forms.CharField(
        widget=forms.TimeInput, min_length=3, max_length=150
    )
    text = forms.Textarea()

    def clean(self):
        """
        Валидация данных
        """
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        email = cleaned_data.get("email")
        topic = cleaned_data.get("topic")
        text = cleaned_data.get("text")
        if name and email and topic and text:
            if (
                valid_text(name) == "is_valid"
                and valid_text(email) == "is_valid"
                and valid_text(topic) == "is_valid"
                and valid_text(text) == "is_valid"
            ):
                if valid_email(email):
                    return cleaned_data
                raise forms.ValidationError("Ведите корректную электронну почту")
            raise forms.ValidationError("Обращение не прошло модерацию")
        raise forms.ValidationError("Поля не могут быть пустыми")

    class Meta:
        model = FeedBackPublic
        fields = ["name", "email", "topic", "text"]


class ReportForm(forms.ModelForm):
    """
    Форма жалобы
    """
    title = forms.CharField(
        widget=forms.TextInput, min_length=3, max_length=50
    )
    text_report = forms.Textarea()

    def clean(self):
        """
        Валидация данных
        """
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text_report = cleaned_data.get("text_report")
        if title and text_report:
            if valid_text(title) == "is_valid" and  valid_text(text_report) == "is_valid":
                return cleaned_data
            raise forms.ValidationError("Обращение не прошло модерацию")
        raise forms.ValidationError("Поле не может быть пустым")
    
    class Meta:
        model = Report
        fields = ["title", "text_report"]
        