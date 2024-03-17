from django.test import TestCase , Client
from django.urls import reverse


class TestIndexPageView(TestCase):
    """
    Тестирование стратовой страницы сайта
    """

    def setUp(self):
        """
        Создание тест пользователя
        """
        self.client = Client()
        self.url = reverse("index")  # Страница index (стартовая)

    def test_index_view(self):
        """
        Проверка доступности cтартовой страницы сайта
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
