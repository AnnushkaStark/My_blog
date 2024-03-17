from django.test import TestCase, Client
from django.urls import reverse

from stories.models import User


class ChangeUserPasswordFormView(TestCase):
    """
    Тестирование представления формы
    смена пароля
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.change_pass_url = reverse("change_password")
        self.user = User.objects.create_user(
            username="testus",
            email="mytest@mail.com",
            password="123testpassS@"
        )
        self.client.login(username="testus", password="123testpassS@")

    def test_change_pass_sucsess(self):
        """
        Успешная смена пароля
        """
        data = {
            "old_pass": "123testpassS@",
            "new_pass": "testpass123S@",
            "new_pass2": " testpass123S@",
        }
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.change_pass_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("settings_page"))
        user = User.objects.get(username="testus")
        user.refresh_from_db()
        self.assertTrue(user.check_password(data["new_pass"]))

    def test_change_pass_failure(self):
        """
        Не успешная смена пароля
        """
        data = {
            "old_pass": "133testpassS@",
            "new_pass": "222testpassS@",
            "new_pass2": "222testpassS@",
        }
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.change_pass_url, data, follow=True)
        self.assertRedirects(response, reverse("settings_page"))
        self.assertContains(response, "Неверный пароль")