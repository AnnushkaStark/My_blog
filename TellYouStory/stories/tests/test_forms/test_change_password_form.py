from django.test import TestCase
from stories.forms import ChangePasswordForm


class TestChangePasswordForm(TestCase):
    """
    Тестирование формы смены пароля
    """

    def test_is_valid_form(self):
        """
        Тестирование валидной формы
        """
        form_data = {
            "old_pass": "Mytmail.com1",
            "new_pass": "Test@testsss1ru",
            "new_pass2": "Test@testsss1ru",
        }
        form = ChangePasswordForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        """
        Тестирование не заполненной формы
        """
        form_data = {
            "old_pass": "",
            "new_pass": "Test@testsss1ru",
            "new_pass2": "",
        }
        form = ChangePasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["old_pass"], ["Обязательное поле."])
        self.assertEqual(form.errors["new_pass2"], ["Обязательное поле."])

    def test_invalid_form(self):
        """
        Тестировние с несовпадающими паролями
        """
        form_data = {
            "old_pass": "Mytmail.com1",
            "new_pass": "Test@testsss1ru",
            "new_pass2": "Yest@testsss1ru",
        }
        form = ChangePasswordForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_uncorrect_form(self):
        """
        Тестировние не проходящего требования к валидации пароля
        """
        form_data = {
            "old_pass": "Mytmail.com1",
            "new_pass": "еest@testsss1ru",
            "new_pass2": "eest@testsss1ru",
        }
        form = ChangePasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
