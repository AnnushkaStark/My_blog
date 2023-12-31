from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.views.generic import FormView, CreateView, ListView
from .forms import UserRegisterForm
from django.contrib.auth.hashers import make_password


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
            return redirect("index")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        """
        Получение данных из формы и сохранение
        пользователя в модели
        """
        try:
            form = UserRegisterForm(request.POST)
            if form.is_valid():                            # Проверка валидности формы
                user = form.save(commit=False)
                password = form.cleaned_data["password"]    
                user.password = make_password(password)      # Хэширование пароля
                user.save()
                messages.success(request, "Создан аккаунт!")
                return redirect("index")
            print(form.errors)
            messages.error(request, "Ошибка ввода данных")
            return redirect("register")
        except TypeError:
            messages.error(request, "Некорректный email или пароль")
            return redirect("register")
        except ValueError:
            messages.error(request, "Ошибка ввода данных")
            return redirect("register")
