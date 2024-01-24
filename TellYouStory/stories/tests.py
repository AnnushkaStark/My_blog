from django.test import TestCase, Client
from .models import User, Biography
from datetime import date
from .forms import (
    UserRegisterForm,
    UserLoginForm,
    ChangeMailForm,
    DeactivateForm,
    ChangeTownForm,
    NameChangeForm,
    FormLinkChange,
    BioChangeForm,
    BirthDateForm,
    AvatarChangeForm,
)
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password, reset_hashers
from django.db.models.fields.files import ImageFieldFile


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
            password="my_password##&&7B",
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
            "password": "testpasswordB5%",
            "password2": "testpasswordB5%",
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
            "password": "testpassword1B%",
            "password2": "wrongpassword1B&",
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
            "password": "testpassword1B@",
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

    def test_uncorrect_username(self):
        """
        Тест некорректного
        имени пользователя
        """
        form_data = {
            "username": "t",
            "email": "tesuser@mail.ru",
            "password": "testpasswordB5%",
            "password2": "testpasswordB5%",
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["username"],
            ["Убедитесь, что это значение содержит не менее 3 символов (сейчас 1)."],
        )


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
        self.user = User.objects.create_user(
            username="tesuser", email="test@mail.ru", password="Test123#passS"
        )
        self.url = reverse("user_page")  # Страница user

    def test_user_page_without_bio(self):
        """
        Проверка доступности страницы user
        и того что при переходе на страницу если у пользователя
        нет биографии она корректно создается
        """
        self.client.login(username="tesuser", password="Test123#passS")
        response = self.client.get(self.url)
        self.biography = Biography(user=self.user)
        self.biography.save()
        biography = Biography.objects.filter(user=self.user).count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(biography, 1)
        self.assertTemplateUsed(response, "user.html")

    def test_user_page_with_bio(self):
        """
        Проверка доступности страницы и отображения биографии
        если она уже есть
        """
        self.biography = Biography(user=self.user, name="Vasya", town="test_town")
        self.biography.save()
        self.client.login(username="tesuser", password="Test123#passS")
        response = self.client.get(self.url)
        biography = Biography.objects.get(user=self.user)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, biography.name)
        self.assertContains(response, biography.town)
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
            "password": "testpassword#!@T1",
            "password2": "testpassword#!@T1",
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
            username="testus", email="mytest@mail.com", password="123testpassS@"
        )

    def test_login_form_view_sucsess(self):
        """
        Успешный вход в систему
        """
        data = {"username": "testus", "password": "123testpassS@"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user_page"))

    def test_login_form_view_failure(self):
        """
        Не успешный вход в систеу
        """
        data = {"username": "testus", "password": "123testS"}

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
            username="testus", email="mytest@mail.com", password="123testpassS@"
        )

        self.client.login(username="testus", password="123testpassS@")

    def test_settings_page_view(self):
        """
        Тестирование доступности страницы настроек аккаунта
        """
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.logout_url)
        self.assertRedirects(response, reverse("index"))


class TestPrivateSettingsPageView(TestCase):
    """
    Тестирование представления
    страницы настроек аккаунта
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.settings_url = reverse("settings_page")
        self.user = User.objects.create_user(
            username="testus", email="mytest@mail.com", password="123testpassS@"
        )

        self.client.login(username="testus", password="123testpassS@")

    def test_settings_page_view(self):
        """
        Тестирование доступности страницы натсроек аккаунта
        """
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.settings_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("settings.html")


class TestSettingsPageView(TestCase):
    """
    Тестирование представления
    страницы настроек профиля
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.private_settings_url = reverse("private_settings_page")
        self.user = User.objects.create_user(
            username="testus", email="mytest@mail.com", password="123testpassS@"
        )

        self.client.login(username="testus", password="123testpassS@")

    def test_private_settings_page_view(self):
        """
        Тестирование доступности страницы натсроек профиля
        """
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.private_settings_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("private_settings.html")


class TestDeactivatePageView(TestCase):
    """
    Тестирование представления
    страницы настроек профиля
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.deactivate_url = reverse("deactivate_page")
        self.user = User.objects.create_user(
            username="testus", email="mytest@mail.com", password="123testpassS@"
        )

        self.client.login(username="testus", password="123testpassS@")

    def test_deactivate_page_view(self):
        """
        Тестирование доступности страницы деактивации аккаунта
        """
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.deactivate_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("deactivate.html")


class TestChangeUserMailForm(TestCase):
    """
    Тестирование формы изменения элекронной почты
    """

    def test_valid_form(self):
        """
        Проверка валидности формы
        """
        form_data = {
            "old_mail": "mytest@mail.com",
            "new_mail": "test@testsss.ru",
        }

        form = ChangeMailForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        """
        Проверка валидности формы при не валидной
        почте
        """

        form_data = {
            "old_mail": "mytmail.com",
            "new_mail": "test@testsss.ru",
        }

        form = ChangeMailForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["old_mail"], ["Введите правильный адрес электронной почты."]
        )

    def test_blank_data(self):
        """
        Тест не заполненной формы
        """
        form = ChangeMailForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["old_mail"], ["Обязательное поле."])
        self.assertEqual(form.errors["new_mail"], ["Обязательное поле."])


class TestChangeUserMailFormView(TestCase):
    """
    Тестирование представление формы
    изменения электронной почты
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.change_mail_url = reverse("change_mail")
        self.user = User.objects.create_user(
            username="testus", email="mytest@mail.com", password="123testpassS@"
        )

        self.client.login(username="testus", password="123testpassS@")

    def test_change_sucsess(self):
        """
        Тест успешное изменение элеткронной почты
        """
        data = {"old_mail": "mytest@mail.com", "new_mail": "123@testpa.ss"}
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.change_mail_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("settings_page"))
        user = User.objects.get(
            email=data["new_mail"]
        )  # Проверяем что почта  изменилась
        self.assertEqual(user.email, data["new_mail"])

    def test_change_failure(self):
        """
        Не успешное изменение почты
        """
        data = {"old_mail": "mytest@mail.com", "new_mail": "123@testpass"}
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.change_mail_url, data, follow=True)
        self.assertFalse(
            User.objects.filter(email="123@testpass").exists()
        )  # Проверяем что почта не изменилась
        self.assertRedirects(response, reverse("settings_page"))
        self.assertContains(response, "Ошибка изменения данных")


class ChangeUserPasswordFormView(TestCase):
    """
    Тестирование представления формы
    смена пароля
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.change_pass_url = reverse("change_password")
        self.user = User.objects.create_user(
            username="testus", email="mytest@mail.com", password="123testpassS@"
        )
        self.client.login(username="testus", password="123testpassS@")

    def test_change_pass_sucsess(self):
        """
        Успешная смена пароля
        """
        data = {
            "old_pass": "123testpassS@",
            "new_pass": "testpass123S@",
            "new_pass2": " testpass123S@",
        }
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.change_pass_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("settings_page"))
        user = User.objects.get(username="testus")
        user.refresh_from_db()
        self.assertTrue(user.check_password(data["new_pass"]))

    def test_change_pass_failure(self):
        """
        Не успешная смена пароля
        """
        data = {
            "old_pass": "133testpassS@",
            "new_pass": "222testpassS@",
            "new_pass2": "222testpassS@",
        }
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.change_pass_url, data, follow=True)
        self.assertRedirects(response, reverse("settings_page"))
        self.assertContains(response, "Неверный пароль")


class TestDeactivateForm(TestCase):
    """
    Тестировние формы деакивации аккаунта
    """

    def test_valid_form(self):
        """
        Тест валидная форма деактивации
        """

        data = {
            "username": "testus",
            "email": "mytest@mail.com",
            "password": "123testpassS@",
            "password2": "123testpassS@",
        }
        form = DeactivateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """
        Тест  не валидная форма деактивации
        """
        data = {
            "username": "testus",
            "email": "mytest@mail.com",
            "password": "123testpassS@",
            "password2": "133testpassS@",
        }
        form = DeactivateForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["password2"], ["Пароли не совпадают"])

    def test_blank_form(self):
        """
        Тест пустая форма деактивации
        """
        form = DeactivateForm(data={})
        self.assertFalse(form.is_valid())
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["username"], ["Обязательное поле."])
        self.assertEqual(form.errors["email"], ["Обязательное поле."])
        self.assertEqual(form.errors["password"], ["Обязательное поле."])
        self.assertEqual(form.errors["password2"], ["Обязательное поле."])


class TestDaectivateFormView(TestCase):
    """
    Тестирование представления формы деактивации
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.deactivate_url = reverse("deactivate_form")
        self.user = User.objects.create_user(
            username="testus", email="mytest@mail.com", password="123testpassS@"
        )
        self.client.login(username="testus", password="123testpassS@")

    def test_deactivate_sucsess(self):
        """
        Успешная деактивация
        """
        data = {
            "username": "testus",
            "email": "mytest@mail.com",
            "password": "123testpassS@",
            "password2": "123testpassS@",
        }
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.deactivate_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("index"))

    def test_deactivate_failure(self):
        """
        Не успешная деактивация не верный пароль
        """
        data = {
            "username": "testus",
            "email": "mytest@mail.com",
            "password": "12testpassS@",
            "password2": "123testpassS@",
        }
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.deactivate_url, data, follow=True)
        self.assertRedirects(response, reverse("deactivate_page"))
        self.assertContains(response, "Ошибка ввода данных")


class TestBiographyModel(TestCase):
    """
    Тестирование  модели биографии пользователя
    """

    def setUp(self):
        """
        Метод данных тест пользоватетеля
        и тест биографии
        """
        self.user = User.objects.create(
            username="testuser",
            email="test@mail.com",
            password="my_password##&&7Q",
        )

        self.bio = Biography.objects.create(
            name="test",
            town="TestCity",
            birth_date="2024-01-07",
            link="https://stepik.org/lesson/1098495/step/5?unit=1109364",
            avatar="test.jpg",
            bio="my_long_long_bio",
            user=self.user,
        )

    def test_bio_creation(self):
        """
        Проверка сохренения в модели объекта биографии
        объекта биография
        """
        self.assertTrue(isinstance(self.user, User))

    def test_models_fields(self):
        """
        Проверка данных содержащихся в полях модели
        """

        self.assertIsInstance(self.bio.name, str)
        self.assertIsInstance(self.bio.town, str)
        self.assertIsInstance(self.bio.birth_date, str)
        self.assertIsInstance(self.bio.link, str)
        self.assertIsInstance(self.bio.avatar, ImageFieldFile)
        self.assertIsInstance(self.bio.bio, str)
        self.assertIsInstance(self.bio.user, User)

    def test_relationship(self):
        """
        Тест связи модели ползователя
          с моделью биографии
        """
        self.assertEqual(self.bio.user, self.user)
        self.assertEqual(self.user, self.bio.user)


class TestChangeNameForm(TestCase):
    """
    Тестирование формы изменения имени пользователя
    """

    def test_valid_form(self):
        """
        Тест валидная форма
        """

        data = {
            "name": "test",
        }
        form = NameChangeForm(data=data)
        self.assertTrue(form.is_valid())


class TestChangeTownForm(TestCase):
    """
    Тестирование формы изменения города пользователя
    """

    def test_valid_form(self):
        """
        Тест валидная форма
        """

        data = {
            "town": "Moscow",
        }
        form = ChangeTownForm(data=data)
        self.assertTrue(form.is_valid())


class TestChangeBio(TestCase):
    """
    Тестирование формы изменения биографии пользователя
    """

    def test_valid_form(self):
        """
        Тест валидная форма
        """

        data = {
            "bio": "bla-bla-bla",
        }
        form = BioChangeForm(data=data)
        self.assertTrue(form.is_valid())


class TestChangeBirthDate(TestCase):
    """
    Тестирование формы изменения даты рождения
    """

    def test_valid_form(self):
        """
        Тест валидная форма
        """

        data = {
            "birth_date": "",  # Поле может быть пустым
        }
        form = BirthDateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """
        Тест  не валидная форма
        """

        data = {
            "birth_date": "1234567",
        }
        form = BirthDateForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["birth_date"], ["Введите правильную дату."])


class TestLinkChangeForm(TestCase):
    """
    Тестирование формы изменения ссылки на соцсеть
    или бусти в профиле пользователя
    """

    def test_valid_form(self):
        """
        Тест валидная форма
        """

        data = {
            "link": "",  # Поле может быть пустым
        }
        form = FormLinkChange(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """
        Тест  не валидная форма
        """

        data = {
            "link": "1234567",
        }
        form = FormLinkChange(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["link"], ["Введите правильный URL."])


class TestChangeAvatarForm(TestCase):
    """
    Тестирование формы изменения фото профиля пользователя
    """

    def test_valid_form(self):
        """
        Тест валидная форма
        """

        data = {
            "avatar": "",  # Поле может быть пустым
        }
        form = AvatarChangeForm(data=data)
        self.assertTrue(form.is_valid())


class TestChangeNameFormView(TestCase):
    """
    Тестирование представления формы
    изменения имени пользователя
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.change_name_url = reverse("change_name")
        self.user = User.objects.create_user(
            username="testus", email="mytest@mail.com", password="123testpassS@"
        )
        self.client.login(username="testus", password="123testpassS@")

    def test_change_name_sucsess(self):
        """
        Успешная смена имени
        """
        data = {
            "name": "test",
        }
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.change_name_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("private_settings_page"))
        biography = Biography.objects.get(name=data["name"])
        self.assertEqual(biography.name, data["name"])


class TestChangeTownFormView(TestCase):
    """
    Тестирвание представление формы
    изменения города пользователя
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.change_town_url = reverse("change_town")
        self.user = User.objects.create_user(
            username="testus", email="mytest@mail.com", password="123testpassS@"
        )
        self.client.login(username="testus", password="123testpassS@")

    def test_change_name_sucsess(self):
        """
        Успешная смена города
        """
        data = {
            "town": "Moscow",
        }
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.change_town_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("private_settings_page"))
        biography = Biography.objects.get(town=data["town"])
        self.assertEqual(biography.town, data["town"])


class TestChangeBiographyFormView(TestCase):
    """
    Тестирование представления формы
    изменения биографии пользователя
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.change_bio_url = reverse("bio_change")
        self.user = User.objects.create_user(
            username="testus", email="mytest@mail.com", password="123testpass@Q"
        )
        self.client.login(username="testus", password="123testpass@Q")

    def test_change_name_sucsess(self):
        """
        Успешная смена биографии
        """
        data = {
            "bio": "bla-bla-bla",
        }
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.change_bio_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("private_settings_page"))
        biography = Biography.objects.get(bio=data["bio"])
        self.assertEqual(biography.bio, data["bio"])


class TestChangeAvatarFormView(TestCase):
    """
    Тестировнание формы изменения фото
    профиля пользовтателя
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.change_avatar_url = reverse("change_avatar")
        self.user = User.objects.create_user(
            username="testus", email="mytest@mail.com", password="123testpassS@"
        )
        self.client.login(username="testus", password="123testpassS@")

    def test_change_name_sucsess(self):
        """
        Успешная смена аватара
        """
        data = {
            "avatar": "",  # Поле может быть пустым
        }
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.change_avatar_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("private_settings_page"))
        biography = Biography.objects.get(avatar=data["avatar"])
        self.assertEqual(biography.avatar, data["avatar"])


class TestChangeBirthDateFormView(TestCase):
    """
    Тестирование формы представления
    изменения даты рождения пользователя
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.change_birth_date_url = reverse("change_birth_date")
        self.user = User.objects.create_user(
            username="testus", email="mytest@mail.com", password="123testpassS@"
        )
        self.client.login(username="testus", password="123testpassS@")

    def test_change_birth_date_sucsess(self):
        """
        Успешная смена даты рождения
        """
        data = {
            "birth_date": "2024-09-01",
        }
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.change_birth_date_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("private_settings_page"))
        biography = Biography.objects.filter(birth_date=data["birth_date"]).count()
        self.assertEqual(biography, 1)

    def test_change_birth_date_failure(self):
        """
        Не успешное изменение даты рождения
        """
        data = {
            "birth_date": "1234567",
        }
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.change_birth_date_url, data, follow=True)
        self.assertRedirects(response, reverse("private_settings_page"))
        self.assertContains(response, "Ошибка ввода данных")


class TestChangeLinkFormView(TestCase):
    """
    Тестирование представления формы изменения ссылки
    на соц сеть или бусти в профиле пользователя
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.change_link_url = reverse("link_change")
        self.user = User.objects.create_user(
            username="testus", email="mytest@mail.com", password="123testpassS@"
        )
        self.client.login(username="testus", password="123testpassS@")

    def test_change_link_sucsess(self):
        """
        Успешное изменение ссылки на соц сеть
        или бусти в профиле пользователя
        """
        data = {
            "link": "",  # Поле может быть пустым
        }
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.change_link_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("private_settings_page"))
        biography = Biography.objects.get(link=data["link"])
        self.assertEqual(biography.link, data["link"])

    def test_change_link_failure(self):
        """
        Не успешное изменение ссылки на соц сеть
        или бусти в профиле пользователя

        """
        data = {
            "link": "1234567",
        }
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.change_link_url, data, follow=True)
        self.assertRedirects(response, reverse("private_settings_page"))
        self.assertContains(response, "Ошибка ввода данных")
