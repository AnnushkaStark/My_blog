from django.test import TestCase, Client
from django.urls import reverse


class TestFeedBackPublicView(TestCase):
    """
    Тестирование доступности страницы
    обратной связи для не аутентифицированного
    пользователя
    """

    def setUp(self):
        """
        Создание тест пользователя
        """
        self.client = Client()
        self.url = reverse("feed_back_page")

    def test_feed_back_view(self):
        """
        Проверка доступности страницы
        обратной связи
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "feed_back.html")




