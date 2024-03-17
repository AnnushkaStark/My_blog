from django.test import TestCase

from stories.forms import BioChangeForm


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
