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


    def test_invalid_text_report(self):
        """
        Тест не валидная форма
        не заполнен текст обращения
        """
        data = {
            "title":"testitle",
            "text_report":""
        }
        form = ReportForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["text_report"], ["Обязательное поле."])

    def test_ban_title_report(self):
        """
        Тест не валидная форма
        нецензурное слово
        в теме письма
        """
        data = {
            "title":"гонорея",
            "text_report":"тестестест"
        }
        form = ReportForm(data=data)
        self.assertFalse(form.is_valid())


    def test_ban_text_report(self):
        """
        Тест не валидная форма
        нецензурное слово
        в теме письма
        """
        data = {
            "title":"тесттест",
            "text_report":"гонорея"
        }
        form = ReportForm(data=data)
        self.assertFalse(form.is_valid())

    def test_blank_report(self):
        """
        Тест не валидная форма
        (пустая)
        """
        data = {
            "title":"",
            "text_report":""
        }
        form = ReportForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["title"], ["Обязательное поле."])
        self.assertEqual(form.errors["text_report"], ["Обязательное поле."])
       


