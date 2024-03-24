from django.test import TestCase

from stories.forms import ReportForm


class TestReportForm(TestCase):
    """
    Тестирование формы жалобы
    """
    def test_valid_form(self):
        """
        Тест валидная форма
        """
        data = {
            "title":"testitle",
            "text_report":"test_report"
        }
        form = ReportForm(data=data)
        self.assertTrue(form.is_valid())
       

    def test_invalid_title(self):
        """
        Тест не валидная форма
        не заполнен заголовок
        """
        data = {
            "title":"",
            "text_report":"test_report"
        }
        form = ReportForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["title"], ["Обязательное поле."])
