from django.test import TestCase

from stories.forms import FeedbackPublicForm


class TestFeedbackPublicForm(TestCase):
    """
    Тестирование формы обратной
    связи  не аутентифицированного
    пользователя
    """

    def test_valid_form(self):
        """
        Тест валидная форма
        """

        data = {
            "name": "test_name",
            "email": "test@mail.com",
            "topic": "test_topic",
            "text": "test.content",
        }
        form = FeedbackPublicForm(data=data)
        self.assertTrue(form.is_valid())

    def test_blank_name(self):
        """
        Тест не валидная форма
        не заполнено имя
        """

        data = {
            "name": "",
            "email": "test@mail.com",
            "topic": "test_topic",
            "text": "test.content",
        }
        form = FeedbackPublicForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["name"], ["Обязательное поле."])

    def test_blank_email(self):
        """
        Тест не валидная форма
        не заполнено имя
        """

        data = {
            "name": "testname",
            "email": "",
            "topic": "test_topic",
            "text": "test.content",
        }
        form = FeedbackPublicForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["email"], ["Обязательное поле."])
    

    def test_blank_topic(self):
        """
        Тест не валидная форма
        не заполнена тема письма
        """

        data = {
            "name": "testname",
            "email": "test@mail.ru",
            "topic": "",
            "text": "test.content",
        }
        form = FeedbackPublicForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["topic"], ["Обязательное поле."])

    def test_blank_text(self):
        """
        Тест не валидная форма
        не заполнено обращение
        """

        data = {
            "name": "testname",
            "email": "test@mail.ru",
            "topic": "testtopic",
            "text": "",
        }
        form = FeedbackPublicForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["text"], ["Обязательное поле."])

    def test_blank_form(self):
        """
        Тест не валидная форма
        (пустая)
        """

        data = {
            "name": "",
            "email": "",
            "topic": "",
            "text": "",
        }
        form = FeedbackPublicForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["name"], ["Обязательное поле."])
        self.assertEqual(form.errors["email"], ["Обязательное поле."])
        self.assertEqual(form.errors["topic"], ["Обязательное поле."])
        self.assertEqual(form.errors["text"], ["Обязательное поле."])

    def test_invalid_mail(self):
        """
        Тест не валидная форма
        кирилица в элетронной
        почте (e)
        """

        data = {
            "name": "testname",
            "email": "tеst@mail.ru",
            "topic": "testtopic",
            "text": "testtext",
        }
        form = FeedbackPublicForm(data=data)
        self.assertFalse(form.is_valid())

    def test_ban_name(self):
        """
        Тест не валидная форма
        нецензурное слово
        вместо имени
        """

        data = {
            "name": "Гонорея",
            "email": "test@mail.ru",
            "topic": "testtopic",
            "text": "testtext",
        }
        form = FeedbackPublicForm(data=data)
        self.assertFalse(form.is_valid())

    def test_ban_topic(self):
        """
        Тест не валидная форма
        нецензурное слово
        в теме письма
        """

        data = {
            "name": "test_name",
            "email": "test@mail.ru",
            "topic": "гонорея",
            "text": "testtext",
        }
        form = FeedbackPublicForm(data=data)
        self.assertFalse(form.is_valid())

    def test_ban_text(self):
        """
        Тест не валидная форма
        нецензурное слово
        в тексте обращения
        """

        data = {
            "name": "test_name",
            "email": "test@mail.ru",
            "topic": "test_topic",
            "text": "гонорея",
        }
        form = FeedbackPublicForm(data=data)
        self.assertFalse(form.is_valid())
