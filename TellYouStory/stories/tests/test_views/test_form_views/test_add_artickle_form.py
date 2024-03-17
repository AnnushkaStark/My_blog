from django.test import TestCase, Client
from django.urls import reverse

from stories.models import User, Story


class TestAddArticleFormView(TestCase):
    """
    Тестирование представления формы
    добавления поста
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.add_story_url = reverse("add_story_form")
        self.user = User.objects.create_user(
            username="testus", email="mytest@mail.com", password="123testpassS@"
        )
        self.client.login(username="testus", password="123testpassS@")

    def test_add_srory_sucsess(self):
        """
        Успешное добвление статьи
        """
        data = {
            "title": "test_title",
            "topic": "test_topic",
            "image": "tast.jpg",
            "content": "test_content",
        }

        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.add_story_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("add_story_page"))
        story = Story.objects.get(author=self.user)
        self.assertEqual(story.author, self.user)

    def test_add_story_failure(self):
        """
        Не успешное добавление статьи
        """
        data = {
            "title": "",
            "topic": "test_topic",
            "image": "tast.jpg",
            "content": "гонорея",
        }

        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.add_story_url, data, follow=True)
        self.assertRedirects(response, reverse("add_story_page"))
        self.assertContains(response, "Контент не прошел модерацию")
