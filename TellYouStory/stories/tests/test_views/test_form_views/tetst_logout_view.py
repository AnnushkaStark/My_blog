from django.test import TestCase, Client
from django.urls import reverse

from stories.models import User


class TestLogoutView(TestCase):
    """
    Тестирование представления logout
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.logout_url = reverse("logout")
        self.user = User.objects.create_user(
            username="testus",
            email="mytest@mail.com",
            password="123testpassS@"
        )

        self.client.login(username="testus", password="123testpassS@")

    def test_settings_page_view(self):
        """
        Тестирование доступности страницы настроек аккаунта
        """
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.logout_url)
        self.assertRedirects(response, reverse("index"))