from django.test import TestCase

from stories.forms import CommentForm


class TestCommentForm(TestCase):
    """
    Тестирование формы комментария
    """
    def test_valid_form(self):
        """
        Тест валидная форма
        """
        data = {
            "text":"test_text"
        }
        
        form = CommentForm(data=data)
        self.assertTrue(form.is_valid())

    def test_blank_form(self):
        """
        Тест пустая форма
        """
        data = {
            "text":""
        }
        
        form = CommentForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["text"], ["Обязательное поле."])

    def test_ban_form(self):
        """
        Тecт нецезурное слово
        """
        data = {
            "text":"гонорея"
        }
        
        form = CommentForm(data=data)
        self.assertFalse(form.is_valid())
      