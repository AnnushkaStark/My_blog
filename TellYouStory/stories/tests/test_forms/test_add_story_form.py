from django.test import TestCase

from stories.forms import AddArticleForm


class TestAddStoryForm(TestCase):
    """
    Тестирование 
    добавления истории
    """

    def test_valid_form(self):
        """
        Тест валидная форма
        """

        data = {
            "title": "test_title",
            "topic": "test_topic",
            "image": "test.jpg",
            "content": "test.content",
        }
        form = AddArticleForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_tile(self):
        """
        Тест  не валидная форма
        не заполнено название
        """

        data = {
            "title": "",
            "topic": "test_topic",
            "image": "test.jpg",
            "content": "test.content",
        }
        form = AddArticleForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["title"], ["Обязательное поле."])

    def test_invalid_form_topic(self):
        """
        Тест  не валидная форма
        не заполнена тема
        """

        data = {
            "title": "test_title",
            "topic": "",
            "image": "test.jpg",
            "content": "test.content",
        }
        form = AddArticleForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["topic"], ["Обязательное поле."])

    def test_invalid_form_no_content(self):
        """
        Тест  не валидная форма
        не заполнены обя поля контент
        и фотография
        """

        data = {
            "title": "test_title",
            "topic": "test_topic",
            "image": "",
            "content": "",
        }
        form = AddArticleForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_ban_title(self):
        """
        Тест  не валидная форма
        нецензурное слово в заголовке
        """

        data = {
            "title": "гонорея",
            "topic": "test_topic",
            "image": "tast.jpg",
            "content": "test_content",
        }
        form = AddArticleForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_ban_tpoic(self):
        """
        Тест  не валидная форма
        нецензурное слово в теме
        """

        data = {
            "title": "test_title",
            "topic": "гонорея",
            "image": "tast.jpg",
            "content": "test_content",
        }
        form = AddArticleForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_ban_content(self):
        """
        Тест  не валидная форма
        нецензурное слово в теме
        """

        data = {
            "title": "test_title",
            "topic": "test_topic",
            "image": "tast.jpg",
            "content": "гонорея",
        }
        form = AddArticleForm(data=data)
        self.assertFalse(form.is_valid())
