from django.test import TestCase

from stories.forms import FormLinkChange


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

