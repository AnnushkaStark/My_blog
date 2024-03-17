from django.test import TestCase , Client
from django.urls import reverse


class TestUserRegistrationView(TestCase):
    """
    Тестирование представления регистрации
    """

    def setUp(self):
        """
        Создание тест пользователя
        """
        self.client = Client()
        self.url = reverse("register")  # Страница  регистрации

    def test_register_view(self):
        """
        Проверка доступности страницы регистрации
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")
