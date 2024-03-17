from django.test import TestCase
from stories.forms import ChangeMailForm
from stories.models import User


class TestChangeUserMailForm(TestCase):
    """
    Тестирование формы изменения элекронной почты
    """

    def setUp(self):
        """
        создание тест
        пользователя
        для проверки
        валидности формы
        с дцбликатом email
        """
        self.duplicate_user = User.objects.create_user(
            username="itsmyname", email="pochta@yandex.ru", password="Simple123!!pass"
        )

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

    def test_uncorrect_email(self):
        """
        тестирование электронной почты на соответствие валидации
        """
        form_data = {
            "old_mail": "mytest@mail.com",
            "new_mail": "test@tes..tsss.ru",
        }
        form = ChangeMailForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_duplicate_mail_form(self):
        """
        Тестирование формы
        с дубликатом электронной почты
        """
        form_data = {
            "old_mail": "mytest@mail.com",
            "new_mail": "pochta@yandex.ru",
        }
        form = ChangeMailForm(data=form_data)
        self.assertFalse(form.is_valid())

