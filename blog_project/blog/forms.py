from django import forms
from .models import User

class ChanceMailForm(forms.Form):
    '''Обработчик формы смены электронной почты'''

    email = forms.EmailField(required=False)
    new_email = forms.EmailField(required=False)
    class Meta:
        model = User
        fields = 'email'
    
        
class ChangePasswordForm(forms.Form):
    '''Обработчик формы смены пароля'''

    password = forms.CharField(required=False)
    new_password = forms.CharField(required=False)