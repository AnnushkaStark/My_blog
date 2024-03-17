from django.test import TestCase

from stories.forms import ChangeTownForm


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