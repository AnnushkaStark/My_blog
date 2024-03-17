from django.test import TestCase, Client
from django.urls import reverse

from stories.models import User, Biography


class TestAddStoryPageView(TestCase):
    """
    Тестирование представления
    страницы добавления поста
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.add_story_url = reverse("add_story_page")
        self.user = User.objects.create_user(
            username="testus",
            email="mytest@mail.com",
            password="123testpassS@"
        )

        self.client.login(username="testus", password="123testpassS@")

    def test_add_story_page_view(self):
        """
        Тестирование доступности страницы
        добавления поста
        """
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.add_story_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("add_story.html")
