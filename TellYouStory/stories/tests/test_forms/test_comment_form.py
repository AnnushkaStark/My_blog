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
            "text_comment":"test_text"
        }
        
        form = CommentForm(data=data)
        self.assertTrue(form.is_valid())