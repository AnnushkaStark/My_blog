from django.test import TestCase, Client
from django.urls import reverse

from stories.models import User


class TestSettingsPageView(TestCase):
    """
    Тестирование представления
    страницы настроек профиля
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.private_settings_url = reverse("private_settings_page")
        self.user = User.objects.create_user(
            username="testus", email="mytest@mail.com", password="123testpassS@"
        )

        self.client.login(username="testus", password="123testpassS@")

    def test_private_settings_page_view(self):
        """
        Тестирование доступности страницы натсроек профиля
        """
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.private_settings_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("private_settings.html")
