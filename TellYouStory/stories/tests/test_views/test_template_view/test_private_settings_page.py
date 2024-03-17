from django.test import TestCase, Client
from django.urls import reverse

from stories.models import User


class TestPrivateSettingsPageView(TestCase):
    """
    Тестирование представления
    страницы настроек аккаунта
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.settings_url = reverse("settings_page")
        self.user = User.objects.create_user(
            username="testus", email="mytest@mail.com", password="123testpassS@"
        )

        self.client.login(username="testus", password="123testpassS@")

    def test_settings_page_view(self):
        """
        Тестирование доступности страницы натсроек аккаунта
        """
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.settings_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("settings.html")