from django.test import TestCase

from stories.forms import UserRegisterForm
from stories.models import User


class TestUserRegistrationForm(TestCase):
    """
    Тестирование формы регистрации пользователя
    """

    def setUp(self):
        """
        Создание тест пользователя
        для проверки дублирующих
        значений email и username

        """
        User.objects.create_user(
            username="user",
            email="testser@mail.com",
            password="Qwerty123^"
        )

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
            "password": "Testpassword1B%",
            "password2": "Wrongpassword1B&",
        }

        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

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

    def test_unorrect_password(self):
        """
        Проверка некорректного пароля
        """
        form_data = {
            "username": "user",
            "email": "tesuser@mail.ru",
            "password": "testpass1",
            "password2": "testpass1",
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_unorrect_email(self):
        """
        Проверка некорректной электронной почты
        """
        form_data = {
            "username": "user1",
            "email": "tesu#ser@mail.ru",
            "password": "testpass123@W",
            "password2": "testpass123@W",
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_duplicate_username(self):
        """
        Тестирование формы с дубликатом username
        """
        form_data = {
            "username": "user",
            "email": "tesuser@mail.ru",
            "password": "testpass123@W",
            "password2": "testpass123@W",
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["username"], ["Пользователь с таким Username уже существует."]
        )

    def test_duplicate_email(self):
        """
        Тестирование формы с дубликатом email
        """
        form_data = {
            "username": "user",
            "email": "tesuser@mail.com",
            "password": "testpass123@W",
            "password2": "testpass123@W",
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

