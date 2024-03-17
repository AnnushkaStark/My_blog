from django.test import TestCase , Client
from django.urls import reverse


class TestLogiPageView(TestCase):
    """
    Тестирование представления страницы входа в систему
    """

    def setUp(self):
        """
        Создание тест пользователя
        """
        self.client = Client()
        self.url = reverse("login_page")  # Страница login

    def test_login_page_view(self):
        """
        Проверка доступности страницы login
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")