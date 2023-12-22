from django import forms
from .models import User, Articles


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

class PostForm(forms.ModelForm):
    """
    Форма загрузки постов пользовтеля
    """
    class Meta:

        model = Articles
        fields = ('title', 'image', 'content')
        
       