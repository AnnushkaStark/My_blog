from django import forms
from .models import User


class BiographyForm(forms.ModelForm):
    """
    Форма добавления биографии
    """
    class Meta:
        model = User
        fields = 'biography',


class AvatarForm(forms.ModelForm):
    """
    Форма загрузки фото
    """
    class Meta:
        model = User
        fields = 'avatar',

