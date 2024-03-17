from django.test import TestCase

from stories.forms import FeedBackUserForm

class TestFeedbackUserForm(TestCase):
    """
    Тестирование формы обратной
    связи аутентифицированного
    пользователя
    """

    def test_valid_form(self):
        """
        Тест валидная форма
        """

        data = {
            "topic": "test_topic",
            "description": "test.content",
        }
        form = FeedBackUserForm(data=data)
        self.assertTrue(form.is_valid())

    def test_blank_topic(self):
        """
        Тест не валидная форма
        поле тема не заполнено
        """

        data = {
            "topic": "",
            "description": "test.content",
        }
        form = FeedBackUserForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["topic"], ["Обязательное поле."])

    def test_blank_description(self):
        """
        Тест не валидная форма
        поле описание  не заполнено
        """

        data = {
            "topic": "test_topic",
            "description": "",
        }
        form = FeedBackUserForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["description"], ["Обязательное поле."])

    def test_blank_form(self):
        """
        Тест не валидная форма
        (пустая форма)
        """

        data = {
            "topic": "",
            "description": "",
        }
        form = FeedBackUserForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["topic"], ["Обязательное поле."])
        self.assertEqual(form.errors["description"], ["Обязательное поле."])

    def test_ban_topic(self):
        """
        Тест не валидная форма
        нецензурное слово в теме письма
        """

        data = {
            "topic": "гонорея",
            "description": "testcontent",
        }
        form = FeedBackUserForm(data=data)
        self.assertFalse(form.is_valid())

    def test_ban_description(self):
        """
        Тест не валидная форма
        нецензурное слово в обращении
        """

        data = {
            "topic": "test_topic",
            "description": "гонорея",
        }
        form = FeedBackUserForm(data=data)
        self.assertFalse(form.is_valid())

