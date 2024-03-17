from django.test import TestCase

from stories.forms import NameChangeForm


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