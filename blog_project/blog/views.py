from django.shortcuts import render, redirect
from django.views.generic.base import View
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password 
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


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
        password = make_password(password)
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
    def post(self,request):
        '''Авторизация пользователя'''
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username = username,password = password)
            if user and user.is_active:
                login(request,user)
                return render(request,'user.html')
            return render(request,'login.html')
        except ValueError:
            return render(request, 'login.html')
        except Exception:
            return render(request, 'login.html')

#------------------------------------------------------------Выход из системы------------------------------------------------
class LogoutView(View):
    '''Выход пользователя из системы'''
    @method_decorator(login_required)
    def post(self,request):
        logout(request)
        return redirect('index.html')

    

 


