from django.test import TestCase, Client
from django.urls import reverse

from stories.models import User


class TestDeactivatePageView(TestCase):
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
        self.deactivate_url = reverse("deactivate_page")
        self.user = User.objects.create_user(
            username="testus", email="mytest@mail.com", password="123testpassS@"
        )

        self.client.login(username="testus", password="123testpassS@")

    def test_deactivate_page_view(self):
        """
        Тестирование доступности страницы деактивации аккаунта
        """
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.deactivate_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("deactivate.html")