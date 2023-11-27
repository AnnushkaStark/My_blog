from django.shortcuts import render, redirect
from django.views.generic.base import View
from .models import User
from django.contrib import messages



# Create your views here.
class IndexPageView(View):
    '''Главная страница проекта'''
    def get(self,request):
      
        return render(request, 'index.html')

#----------------------------------------------------Страница регистрации---------------------------------------------------

class RegisterView(View):
    '''Страница регистрации пользователя'''
    def get(self,request):
        return  render(request, 'reg.html')

    def post(self,request):
        '''Обработка формы регистрации пользовтеля'''
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username = username).exists():
            return render(request,'reg.html')
        if User.objects.filter(email=email).exists():
            return render(request,'reg.html')
        user= User.objects.create(username= username, email= email, password= password)
        user.save()
        return render(request,'login.html')
        
 #-------------------------------------------------------Вход в личный кабинет---------------------------------------------

class LoginView(View):
    '''Страница входа пользователя'''
    def get(self,request):

        return render(request, 'login.html')
