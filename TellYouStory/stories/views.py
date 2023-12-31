from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.views.generic import FormView, CreateView, ListView
from django.contrib.auth.views import LogoutView
from django.views import View
from .forms import (
    UserRegisterForm,
    UserLoginForm,
    ChangeMailForm,
    ChangePasswordForm,
    DeactivateForm,
    NameChangeForm,
    ChangeTownForm,
    BirthDateForm,
    FormLinkChange,
    AvatarChangeForm,
    BioChangeForm,
)
from django.contrib.auth.hashers import make_password, check_password, reset_hashers
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, Biography


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


class ChangePasswordFormView(FormView, LoginRequiredMixin):
    """
    Представление формы смены пароляпользователя
    """

    def post(self, request):
        """
        Получение данных из формы
        """
        user = User.objects.get(id=request.user.id)
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_pasword = form.cleaned_data["old_pass"]
            if user.check_password(old_pasword):
                new_password = form.cleaned_data["new_pass"]
                user.set_password(new_password)
                user.save()
                messages.success(request, "Ваш пароль изменен")
                return redirect("settings_page")
            messages.error(request, "Неверный пароль")
            return redirect("settings_page")
        messages.error(request, "Ошибка изменения данных")
        return redirect("settings_page")


class DeactivateFormView(FormView, LoginRequiredMixin):
    """
    Представление формы деактивации аккаунта
    """

    def post(self, request):
        """
        Получение данных из формы
        """
        user = User.objects.get(id=request.user.id)
        form = DeactivateForm(request.POST)
        if form.is_valid():
            old_pasword = form.cleaned_data["password"]
            if user.check_password(old_pasword):
                user.is_active = False
                user.save()
                messages.success(request, "Ваш aккаунт деактивирован")
                return redirect("index")
            messages.error(request, "Неверный пароль")
            return redirect("deactivate_page")
        messages.error(request, "Ошибка ввода данных")
        return redirect("deactivate_page")


class NameChangeFormView(FormView, LoginRequiredMixin):
    """
    Представление формы изменения пользователя в
    настройках профиля
    """

    def post(self, request):
        """
        Получение данных из формы
        """
        try:
            user = request.user
            biography = Biography.objects.get(user=request.user)
            form = NameChangeForm(request.POST, request.FILES)
            if form.is_valid():
                biography.name = form.cleaned_data["name"]
                biography.save()
                messages.success(request, "Данные имени обновлены")
                return redirect("private_settings_page")
            messages.error(request, "Ошибка ввода данных")
            messages.success(request, "Данные имени обновлены")
            return redirect("private_settings_page")
        except Biography.DoesNotExist:
            form = NameChangeForm(request.POST, request.FILES)
            if form.is_valid():
                biography = Biography.objects.create(
                    name=form.cleaned_data["name"], user_id=request.user.id
                )
                biography.save()
                messages.success(request, "Данные профиля обновлены")
                return redirect("private_settings_page")
            messages.error(request, "Ошибка ввода данных")
            return redirect("private_settings_page")


class TownChangeFormView(FormView, LoginRequiredMixin):
    """
    Представление формы изменения пользователя в
    настройках профиля
    """

    def post(self, request):
        """
        Получение данных из формы
        """
        try:
            user = request.user
            biography = Biography.objects.get(user=request.user)
            form = ChangeTownForm(request.POST, request.FILES)
            if form.is_valid():
                biography.town = form.cleaned_data["town"]
                biography.save()
                messages.success(request, "Данные города обновлены")
                return redirect("private_settings_page")
            messages.error(request, "Ошибка ввода данных")
            return redirect("private_settings_page")
        except Biography.DoesNotExist:
            form = ChangeTownForm(request.POST, request.FILES)
            if form.is_valid():
                biography = Biography.objects.create(
                    town=form.cleaned_data["town"], user_id=request.user.id
                )
                biography.save()
                messages.success(request, "Данные города обновлены")
                return redirect("private_settings_page")
            messages.error(request, "Ошибка ввода данных")
            return redirect("private_settings_page")


class ChangeBirthDateFormView(FormView, LoginRequiredMixin):
    """
    Изменение даты рождения в профиле пользователя
    """

    def post(self, request):
        """
        Получение данных из формы
        """
        try:
            user = request.user
            biography = Biography.objects.get(user=request.user)
            form = BirthDateForm(request.POST, request.FILES)
            if form.is_valid():
                biography.birth_date = form.cleaned_data["birth_date"]
                biography.save()
                messages.success(request, "Данные даты рождения обновлены")
                return redirect("private_settings_page")
            messages.error(request, "Ошибка ввода данных")
            return redirect("private_settings_page")
        except Biography.DoesNotExist:
            form = BirthDateForm(request.POST, request.FILES)
            if form.is_valid():
                biography = Biography.objects.create(
                    birth_date=form.cleaned_data["birth_date"], user_id=request.user.id
                )
                biography.save()
                messages.success(request, "Данные даты рождения обновлены")
                return redirect("private_settings_page")
            messages.error(request, "Ошибка ввода данных")
            return redirect("private_settings_page")


class ChangeLinkFormView(FormView, LoginRequiredMixin):
    """
    Представление формы измененния ссылки на соцсеть или
    бусти в профиле пользователя
    """

    def post(self, request):
        """
        Получение данных из формы
        """
        try:
            user = request.user
            biography = Biography.objects.get(user=request.user)
            form = FormLinkChange(request.POST, request.FILES)
            if form.is_valid():
                biography.link = form.cleaned_data["link"]
                biography.save()
                messages.success(request, "Данные ссылки обновлены")
                return redirect("private_settings_page")
            messages.error(request, "Ошибка ввода данных")
            return redirect("private_settings_page")
        except Biography.DoesNotExist:
            form = FormLinkChange(request.POST, request.FILES)
            if form.is_valid():
                biography = Biography.objects.create(
                    link=form.cleaned_data["link"], user_id=request.user.id
                )
                biography.save()
                messages.success(request, "Данные ссылки обновлены")
                return redirect("private_settings_page")
            messages.error(request, "Ошибка ввода данных")
            return redirect("private_settings_page")


class AvatarFormView(FormView, LoginRequiredMixin):
    """
    Представления формы изменения фото профиля пользователя
    """

    def post(self, request):
        """
        Получение данных из формы
        """
        try:
            user = request.user
            biography = Biography.objects.get(user=request.user)
            form = AvatarChangeForm(request.POST, request.FILES)
            if form.is_valid():
                biography.avatar = form.cleaned_data["avatar"]
                biography.save()
                messages.success(request, "Фото профиля обновлено")
                return redirect("private_settings_page")
            messages.error(request, "Ошибка ввода данных")
            return redirect("private_settings_page")
        except Biography.DoesNotExist:
            form = AvatarChangeForm(request.POST, request.FILES)
            if form.is_valid():
                biography = Biography.objects.create(
                    avatar=form.cleaned_data["avatar"], user_id=request.user.id
                )
                biography.save()
                messages.success(request, "Фото профиля обновлено")
                return redirect("private_settings_page")
            messages.error(request, "Ошибка ввода данных")
            return redirect("private_settings_page")


class BioChangeFormView(FormView, LoginRequiredMixin):
    """
    Представление формы изменения биографии пользователя
    """

    def post(self, request):
        """
        Получение данных из формы
        """
        try:
            user = request.user
            biography = Biography.objects.get(user=request.user)
            form = BioChangeForm(request.POST, request.FILES)
            print(form)
            if form.is_valid():
                biography.bio = form.data["bio"]
                biography.save()
                messages.success(request, "Биография обновлена")
                print(form)
                return redirect("private_settings_page")

            print(form)
            messages.error(request, "Ошибка ввода данных")
            return redirect("private_settings_page")
        except Biography.DoesNotExist:
            form = BioChangeForm(request.POST, request.FILES)
            if form.is_valid():
                biography = Biography.objects.create(
                    bio=form.data["bio"], user_id=request.user.id
                )
                biography.save()
                messages.success(request, "Биография обновлена")
                return redirect("private_settings_page")
            messages.error(request, "Ошибка ввода данных")
            return redirect("private_settings_page")
        except KeyError:
            print(form.data)
            return redirect("private_settings_page")
