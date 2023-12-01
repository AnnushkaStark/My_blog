from django import forms
from .models import User


class BiographyForm(forms.ModelForm):
    class Meta:
        model = User
        fields = 'biography',
