from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.views.generic import FormView, CreateView, ListView
from django.contrib.auth.views import LogoutView
from django.views import View
from .forms import UserRegisterForm, UserLoginForm, ChangeMailForm
from django.contrib.auth.hashers import make_password, check_password, reset_hashers
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User


# Create your views here.


class IndexPageView(TemplateView):
    """
    Представление стратовой страницы сайта
    """

    template_name = "index.html"


class RegisterPageView(TemplateView):
    """
    Представление сраницы регистрации -
    звгрузка страницы  при переходе по ссылке
    запрос GET
    """

    template_name = "register.html"


class UserRegistrationViwe(FormView):
    """
    Представление формы регистрации пользователя
    """

    def dispatch(self, request, *args, **kwargs):
        """
        Если пользоваетель уже зарегистрирован
        возврат на страницу индекс
        """
        if request.user.is_authenticated:
            messages.error(request, "Пользователь уже существует")
            return redirect("index")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        """
        Получение данных из формы и сохранение
        пользователя в модели
        """
        try:
            form = UserRegisterForm(request.POST)
            if form.is_valid():  # Проверка валидности формы
                user = form.save(commit=False)
                password = form.cleaned_data["password"]
                user.password = make_password(password)  # Хэширование пароля
                user.save()
                messages.success(request, "Создан аккаунт!")
                return redirect("login_page")
            print(form.errors)
            messages.error(request, "Ошибка ввода данных")
            return redirect("register")
        except TypeError:
            messages.error(request, "Некорректный email или пароль")
            return redirect("register")
        except ValueError:
            messages.error(request, "Ошибка ввода данных")
            return redirect("register")


class UserLoginView(TemplateView):
    """
    Представление страницы login
    Запрос GET
    """

    template_name = "login.html"


class UserLogoutView(LogoutView, LoginRequiredMixin):
    """
    Представление выхода пользователя из системы
    """

    http_method_names = ["post"]

    def dispatch(self, request, *args, **kwargs):
        """
        Если пользоваетель уже залогинен
        выводит пользователя из системы
        """
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, "Спасибо за проведенное время!")
            return redirect("index")
        messages.error(request, "Ошибка входа из системы")
        return redirect("user")


class UserLoginFormView(FormView):
    """
    Обработка формы login
    """

    def dispatch(self, request, *args, **kwargs):
        """
        Если пользоваетель уже зарегистрирован
        возврат на страницу индекс
        """
        if request.user.is_authenticated:
            messages.error(request, "Вы уже вошли в систему")
            return redirect("user")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        """
        Получение данных из формы и
        login пользователя на сайте
        """
        try:
            form = UserLoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data["username"]  # Получение данных из формы
                password = form.cleaned_data["password"]
                user = authenticate(
                    request, username=username, password=password
                )  # Аутентификация пользователя
                if (
                    user is not None and user.is_active
                ):  # Если пользователь зарегистрирован
                    login(request, user)
                    messages.success(request, f"Привет {username}!")  # Вход в систему
                    return redirect("user_page")
            messages.error(request, "Ошибка входа ")
            return redirect("login_page")
        except TypeError:
            messages.error(request, "Ошибка входа")
            return redirect("login_page")
        except ValueError:
            messages.error(request, "Ошибка входа")
            return redirect("login_page")


class UserPageView(TemplateView, LoginRequiredMixin):
    """
    Личный кабинет пользователя запрос GET
    """

    template_name = "user.html"


class SettingsPage(TemplateView, LoginRequiredMixin):
    """
    Cтраница настроек аккаунта (запрос get)
    """

    template_name = "settings.html"


class PrivateSettingsPage(TemplateView, LoginRequiredMixin):
    """
    Страница  насроек профиля (запрос get)
    """

    template_name = "private_settings.html"


class DeactivatePage(TemplateView, LoginRequiredMixin):
    """
    Страница деактивации аккаунта (запрос get)
    """

    template_name = "deactivate.html"


class ChangeMailFormView(FormView, LoginRequiredMixin):
    """
    Представление смены электронной почты пользователя
    """

    def post(self, request):
        """
        Получение данных из формы смены
        электронной почты
        """
        user = User.objects.get(id=request.user.id)
        form = ChangeMailForm(request.POST)
        if form.is_valid():
            old_mail = form.cleaned_data["old_mail"]
            new_mail = form.cleaned_data["new_mail"]
            if user.email == old_mail:
                user.email = new_mail
                user.save()
                messages.success(request, "Ваша электронная почта изменена")
                return redirect("settings_page")
            messages.error(request, "Неверная почта")
            return redirect("settings_page")
        messages.error(request, "Ошибка изменения данных")
        return redirect("settings_page")
