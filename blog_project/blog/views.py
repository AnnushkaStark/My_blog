from django.shortcuts import render
from django.views.generic.base import View

# Create your views here.
class IndexPageView(View):
    '''Главная страница проекта'''
    def get(self,request):
      
        return render(request, 'index.html')

class RegisterView(View):
    '''Страница регистрации пользователя'''
    def get(self,request):

        return  render(request, 'reg.html')
    
class LoginView(View):
    '''Страница входа пользователя'''
    def get(self,request):

        return render(request, 'login.html')
