from django.test import TestCase
from stories.forms import UserLoginForm


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
        form = UserLoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["username"], ["Обязательное поле."])
        self.assertEqual(form.errors["password"], ["Обязательное поле."])
