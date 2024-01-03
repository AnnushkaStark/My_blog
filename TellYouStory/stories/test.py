from django.test import TestCase, Client
from .models import User
from .forms import UserRegisterForm, UserLoginForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login


class TestUserModel(TestCase):
    """
    Teст модели пользователя
    """

    def setUp(self):
        """
        Метод данных тест пользоватетеля
        """
        self.user = User.objects.create(
            username="testuser",
            email="test@mail.com",
            password="my_password##&&7",
        )

    def test_user_creation(self):
        """
        Проверка сохренения в модели объекта User
        """
        self.assertTrue(isinstance(self.user, User))

    def test_models_fields(self):
        """
        Проверка данных содержащихся в полях модели
        """

        self.assertIsInstance(self.user.username, str)
        self.assertIsInstance(self.user.email, str)
        self.assertIsInstance(self.user.password, str)
        self.assertIsInstance(self.user.is_verificate, bool)
        self.assertIsInstance(self.user.is_superuser, bool)
        self.assertIsInstance(self.user.is_active, bool)


class TestUserRegistrationForm(TestCase):
    """
    Тестирование формы регистрации пользователя
    """

    def test_valid_form(self):
        """
        Проверка валидности формы
        """
        form_data = {
            "username": "testuser",
            "email": "tesuser@mail.ru",
            "password": "testpassword",
            "password2": "testpassword",
        }

        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blalnk_form(self):
        """
        Проверка отправки не заполненной  формы
        """
        form = UserRegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["username"], ["Обязательное поле."])
        self.assertEqual(form.errors["email"], ["Обязательное поле."])
        self.assertEqual(form.errors["password"], ["Обязательное поле."])
        self.assertEqual(form.errors["password2"], ["Обязательное поле."])

    def test_invalid_password(self):
        """
        Тестирование несовпадения пароля
        и подтверждения пароля
        """
        form_data = {
            "username": "testuser",
            "email": "tesuser@mail.ru",
            "password": "testpassword",
            "password2": "wrongpassword",
        }

        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["password2"], ["Пароли не совпадают"])


class TestUserLoginForm(TestCase):
    """
    Тестирование формы login
    """

    def test_valid_form(self):
        """
        Проверка валидности формы
        """
        form_data = {
            "username": "testuser",
            "password": "testpassword",
        }

        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blalnk_form(self):
        """
        Проверка отправки не заполненной  формы
        """
        form = UserRegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["username"], ["Обязательное поле."])
        self.assertEqual(form.errors["password"], ["Обязательное поле."])


class TestUserRegistrationView(TestCase):
    """
    Тестирование представления регистрации
    """

    def setUp(self):
        """
        Создание тест пользователя
        """
        self.client = Client()
        self.url = reverse("register")  # Страница  регистрации

    def test_register_view(self):
        """
        Проверка доступности страницы регистрации
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")


class TestIndexPageView(TestCase):
    """
    Тестирование стратовой страницы сайта
    """

    def setUp(self):
        """
        Создание тест пользователя
        """
        self.client = Client()
        self.url = reverse("index")  # Страница index (стартовая)

    def test_index_view(self):
        """
        Проверка доступности cтартовой страницы сайта
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")


class TestLogiPageView(TestCase):
    """
    Тестирование представления страницы входа в систему
    """

    def setUp(self):
        """
        Создание тест пользователя
        """
        self.client = Client()
        self.url = reverse("login_page")  # Страница login

    def test_login_page_view(self):
        """
        Проверка доступности страницы login
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")


class TestUserPageView(TestCase):
    """
    Тестирование представления страницы пользователя
    """

    def setUp(self):
        """
        Создание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")  # Страница user

    def test_login_page_view(self):
        """
        Проверка доступности страницы user
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user.html")


class TestUserRegistrationFormView(TestCase):
    """
    Тестирование предствления формы регистрации пользоватея
    """

    def setUp(self):
        """
        Создание тест пользователя
        """
        self.url = reverse("register_form")
        self.data = {
            "username": "tesuser",
            "email": "test@mail.com",
            "password": "testpassword#!@",
            "password2": "testpassword#!@",
        }

    def test_register_form_view_sucsess(self):
        """
        Проверка успешной регистрации
        """
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login_page"))
        user = User.objects.get(username=self.data["username"])
        self.assertEqual(user.email, self.data["email"])
        self.assertTrue(user.check_password(self.data["password"]))

    def test_register_form_view_failure(self):
        """
        Тестирование регистрации при не валидной форме
        """
        invalid_data = self.data.copy()
        invalid_data["password2"] = "wrongpassword"
        response = self.client.post(self.url, data=invalid_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("register"))
        self.assertContains(response, "Ошибка ввода данных")
        self.assertFalse(User.objects.filter(username="tesuser").exists())

    def test_blank_data(self):
        """
        Тестирование попытки регистрации
        c  не валидной формой ( пустой юзернейм)
        """
        blank_data = self.data.copy()
        blank_data["username"] = ""
        response = self.client.post(self.url, data=blank_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("register"))
        self.assertContains(response, "Ошибка ввода данных")


class TestLoginFormView(TestCase):
    """
    Тестирование  представления формы login
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.login_url = reverse("login_form")
        self.user = User.objects.create_user(
            username="testus", email="mytest@mail.com", password="123testpass"
        )

    def test_login_form_view_sucsess(self):
        """
        Успешный вход в систему
        """
        data = {"username": "testus", "password": "123testpass"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user_page"))

    def test_login_form_view_failure(self):
        """
        Не успешный вход в систеу
        """
        data = {"username": "testus", "password": "123test"}

        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login_page"))


class TestLogoutView(TestCase):
    """
    Тестирование представления logout
    """
    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.logout_url = reverse("logout")
        self.user = User.objects.create_user(
            username="testus", email="mytest@mail.com", password="123testpass"
        )

        self.client.login( username="testus",password="123testpass")

    def test_logout_view(self):
        """
        Тестирование выхода из системы
        """
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code,200)
        response = self.client.post(self.logout_url)
        self.assertRedirects(response,reverse("index"))


