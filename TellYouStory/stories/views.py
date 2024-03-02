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
    AddArticleForm,
    FeedBackUserForm,
    FeedbackPublicForm,
)
from django.contrib.auth.hashers import make_password, check_password, reset_hashers
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, Biography, Story


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
        return redirect("user_page")


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
            return redirect("user_page")
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


class UserPageView(ListView, LoginRequiredMixin):
    """
    Личный кабинет пользователя запрос GET
    """

    def get(self, request, *args, **kwargs):
        """
        Вывод биографии пользователя на страницу
        """
        try:
            user = request.user
            biography = Biography.objects.get(user=user)
            if biography:
                return render(request, "user.html", {"biography": biography})
            else:
                biography = Biography(user=user)
                biography.save()
                biography = Biography.objects.get(user=user)
                return render(request, "user.html", {"biography": biography})
        except Biography.DoesNotExist:
            biography = Biography(user=user)
            biography.save()
            biography = Biography.objects.get(user=user)
            return render(request, "user.html", {"biography": biography})


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
                update_session_auth_hash(request, user)
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
            if form.is_valid():
                biography.bio = form.data["bio"]
                biography.save()
                messages.success(request, "Биография обновлена")
                return redirect("private_settings_page")
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
            return redirect("private_settings_page")


class AddStoryPage(TemplateView, LoginRequiredMixin):
    """
    Cтраница добавления поста ( запрос пост)
    """

    template_name = "add_story.html"


class AddStoryFormView(FormView, LoginRequiredMixin):
    """
    Представление формы добавления статьи
    """

    def post(self, request):
        """
        Функция добвления поста
        """
        form = AddArticleForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.save()
            messages.success(request, "История успешно опубликована")
            return redirect("add_story_page")
        messages.error(request, "Контент не прошел модерацию")
        return redirect("add_story_page")


class FeedBackPageView(TemplateView):
    """
    Представление страницы обратной связи
    """

    template_name = "feed_back.html"


class FeedBackUserFormView(FormView, LoginRequiredMixin):
    """
    Представление формы отправления
    обратной связи для аутентифицированного пользователя
    """

    def post(self, request):
        """
        Функция отправления обратной
        связи
        """
        form = FeedBackUserForm(request.POST, request.FILES)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(
                request, "Обращение отправлено, ответим вам на электронную почту"
            )
            return redirect("feed_back_page")
        messages.error(request, "Обращение не прошло модерацию")
        return redirect("feed_back_page")


class FeedBackPublicFormView(FormView):
    """
    Представление формы отправки обратной
    связи для не аутентифицированного пользователя
    """

    def post(self, request):
        """
        Функция отправления обратной
        связи
        """
        form = FeedbackPublicForm(request.POST, request.FILES)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.save()
            messages.success(
                request, "Обращение отправлено, ответим вам на электронную почту"
            )
            return redirect("feed_back_page")
        messages.error(request, "Обращение не прошло модерацию")
        return redirect("feed_back_page")


class ArticleRankListView(ListView, LoginRequiredMixin):
    """
    Представление вывода
    на страницу статей
    в порядке ранжирвания
    """

    def get(self, request):
        """
        Получение списка статей
        """
        articles = Story.objects.all().order_by("-rank")

        return render(request, "list_story_rank.html", {"articles": articles})


class ArticleTimeListView(ListView, LoginRequiredMixin):
    """
    Представление вывода
    на страницу статей
    хронологическом порядке
    """

    def get(self, request):
        """
        Получение списка статей
        """
        articles = Story.objects.all().order_by("-date_create")

        return render(request, "list_story_rank.html", {"articles": articles})


class ArticleTopicTimeView(ListView, LoginRequiredMixin):
    """
    Представление вывода
    на страницу всех статей
    по тематике  упорядчиванием
    по хронологии
    """

    def get(self, request, topic):
        """
        Получение списка статей  по теме
        """
        articles = Story.objects.filter(topic=topic).order_by("-date_create").all()

        return render(request, "topic_time.html", {"articles": articles})


class ArticleAuthorTimeView(ListView, LoginRequiredMixin):
    """
    Представление вывода
    на страницу всех статей
    определенного автра
    с  упорядчиванием
    по хронологии
    """

    def get(self, request, author_id):
        """
        Получение списка статей  автора
        """
        articles = (
            Story.objects.filter(author_id=author_id).order_by("-date_create").all()
        )

        return render(request, "article_author.html", {"articles": articles})


class AuthorPageView(ListView, LoginRequiredMixin):
    """
    Представление страницы с выводом информации
    об авторе статьи
    """

    def get(self, request, author_id):
        """
        Получение биографии определенного
        автора
        """
        biography = Biography.objects.get(user_id=author_id)

        return render(request, "author_info.html", {"biography": biography})


class MyStoriesView(LoginRequiredMixin, ListView):
    """
    Представление страницы собтвенных
    статей автора
    """

    def get(self, request):
        """
        Выборка статей пользоватея
        """

        articles = (
            Story.objects.filter(author=request.user).order_by("-date_create").all()
        )
        if len(articles):
            return render(request, "my_news.html", {"articles": articles})

        messages.error(request, "У вас еще нет своих статей, добавьте первую историю")
        return redirect("add_story_page")


class MySingleStoryView(ListView, LoginRequiredMixin):
    """
    Представление перехода
    страницу статьи
    в личном кабинете
    автора
    """

    def get(serl, request, article_id):
        """
        Получение одной статьи
        по ID
        """
        article = Story.objects.filter(
            id=article_id, author=request.user, is_public=True
        )
        return render(request, "my_story.html", {"article": article})
