from django.test import TestCase

from stories.forms import AvatarChangeForm

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
