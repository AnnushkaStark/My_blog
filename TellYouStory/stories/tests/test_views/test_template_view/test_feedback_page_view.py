from django.test import TestCase, Client
from django.urls import reverse


from stories.models import User



class TestFeedBackUserPageView(TestCase):
    """
    Тестирование доступности страницы
    добавления обратной связи
    для аутентифицированного пользователя
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.add_feed_back_url = reverse("feed_back_page")
        self.user = User.objects.create_user(
            username="testus", email="mytest@mail.com", password="123testpassS@"
        )

        self.client.login(username="testus", password="123testpassS@")

    def test_add_feed_page_view(self):
        """
        Тестирование доступности страницы
        оставления обратной связи
        """
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.add_feed_back_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("feed_back.html")