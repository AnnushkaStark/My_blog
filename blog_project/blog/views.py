from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic.edit import FormView
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import ChanceMailForm ,ChangePasswordForm



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
            if user:
                login(request,user)
                return render(request,'user.html')
            return render(request,'login.html')
        except ValueError:
            return render(request, 'login.html')
        except Exception:
            return render(request, 'login.html')

#------------------------------------------------------------Выход из системы--------------------------------------------------------
class LogoutView(View):
    '''Выход пользователя из системы'''
    @method_decorator(login_required)
    def post(self,request):
        logout(request)
        return redirect('index.html')

#---------------------------------------------------------Настройки аккаунта-----------------------------------------------------------

class AccountSettingView(View):
    '''Страница настроек аккаунта'''
    
    @method_decorator(login_required)
    def get(self,request):

        return render(request,'account_settings.html')
   
class ChangeEamail(FormView):

    '''Обработчик формы изменения почты пользвоателя''' 

    @method_decorator(login_required)
    def post(self,request):
        try:
            user = request.user
            old_mail = request.POST.get('old_mail')
            new_mail = request.POST.get('new_mail')
            user_mail = user= User.objects.get(id= user.id)
            if old_mail == user.email:
                user= User.objects.get(id= user.id)
                user.email = new_mail
                user.save()
                
                return redirect('settings')
            else:
                return redirect('settings') 
    
        except Exception:
            return render(request,'user.html')
      

class ChangePassword(FormView):
    '''Обработка формы смены пароля'''
    
    @method_decorator(login_required)
    def post(self,request):
        try:
            user = request.user
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            new_password_2 = request.POST.get('new_password_two')
            user= User.objects.get(id= user.id)
            if  new_password == new_password_2 and  user.check_password(old_password):
                user= User.objects.get(id= user.id)
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request,user)
                return redirect('settings')
            return redirect('user')
        except Exception:
            return render(request,'user.html')
 


