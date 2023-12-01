from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import generic, View
from .models import User
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.hashers import make_password


# -----Главная страница-----
class IndexPageView(generic.TemplateView):
    """
    Главная страница проекта

    Заменил View на TemplateView
    """
    template_name = 'blog/index.html'


# -----Страница регистрации-----
class RegisterView(generic.TemplateView):
    """
    Страница регистрации пользователя

    Заменил View на TemplateView
    Добавил метод dispatch срабатывающий перед инициализацией вьюхи
    Если юзер уже авторизован, то его перебрасывает на главную.
    """
    template_name = 'blog/reg.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Обработка формы регистрации пользователя"""
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = make_password(request.POST.get('password'))
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return render(request, self.template_name)
        user = User.objects.create(username=username, email=email, password=password)
        user.save()
        return redirect('login')


# -----Вход в личный кабинет-----
class LoginView(generic.TemplateView):
    """
    Страница входа пользователя

    Заменил View на TemplateView
    Добавил метод dispatch срабатывающий перед инициализацией вьюхи
    Если юзер уже авторизован, то его перебрасывает на главную.
    """
    template_name = 'blog/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Авторизация пользователя"""
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')
            return self.get(request, *args, **kwargs)
        except ValueError:
            return self.get(request, *args, **kwargs)
        except Exception:
            return self.get(request, *args, **kwargs)


# -----Выход из системы-----
# Снёс к чертям

# -----Настройки аккаунта-----
class AccountSettingView(LoginRequiredMixin, generic.TemplateView):
    """
    Страница настроек аккаунта

    Заменил View на TemplateView
    Добавил миксин проверяющий залогинен юзер или нет
    """
    template_name = 'blog/account_settings.html'


class ChangeEmail(LoginRequiredMixin, generic.View):
    """
    Обработчик формы изменения почты пользователя

    Добавил миксин проверяющий залогинен юзер или нет
    """

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            old_mail = request.POST.get('old_mail')
            new_mail = request.POST.get('new_mail')
            if old_mail == user.email:
                user.email = new_mail
                user.save()
                return redirect('settings')
            else:
                return redirect('settings')

        except Exception:
            return redirect('index')


class ChangePassword(LoginRequiredMixin, generic.View):
    """
    Обработка формы смены пароля

    Добавил миксин проверяющий залогинен юзер или нет
    """

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            new_password_2 = request.POST.get('new_password_two')
            if new_password == new_password_2 and user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                return redirect('settings')
            return redirect('index')
        except Exception:
            return redirect('index')


class AddBio(LoginRequiredMixin, generic.View):
    """
    Обработка формы добавления биографии

    Добавил миксин проверяющий залогинен юзер или нет
    """

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            biography = request.POST.get('biography')
            user.biography = biography
            user.save()
            return redirect('settings')

        except Exception:
            return redirect('index')
