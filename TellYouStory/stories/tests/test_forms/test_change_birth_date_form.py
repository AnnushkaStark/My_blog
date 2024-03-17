from django.test import TestCase

from stories.forms import  BirthDateForm

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
