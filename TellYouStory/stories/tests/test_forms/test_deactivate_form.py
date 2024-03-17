from django.test import TestCase
from stories.forms import DeactivateForm



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
