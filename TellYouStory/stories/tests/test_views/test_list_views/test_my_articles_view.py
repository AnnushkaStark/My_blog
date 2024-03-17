from django.test import TestCase, Client
from django.urls import reverse

from stories.models import User, Story


class TestMyStoriesView(TestCase):
    """
    Тестирование представления
    вывода статей автора в личном кабинете
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username="testus", email="mytest@mail.com", password="123testpassS@"
        )
        self.another_user = User.objects.create_user(
            username="testuser_1", email="mytest@mail.ru", password="321testpassS@"
        )
        self.article_1 = Story.objects.create(
            title="test_title_1",
            topic="testopic_1",
            image="test_image",
            author=self.user,
            like_counter=10,
            dislike_counter=0,
            comment_counter=10,
            views_counter=10,
        )
        self.article_1.rank = self.article_1.get_rank()
        self.article_1.save()

        self.article_2 = Story.objects.create(
            title="test_title_2",
            topic="testopic_2",
            image="test_image",
            author=self.another_user,
            like_counter=10,
            dislike_counter=0,
            comment_counter=10,
            views_counter=10,
        )
        self.article_2.rank = self.article_2.get_rank()
        self.article_2.save()

        self.news_url = reverse("my_stories")

    def test_my_story_page(self):
        """
        Проверка доступности
        старницы вывода статей
        автора в личном кабинете
        """
        self.client.login(username="testus", password="123testpassS@")
        response = self.client.get(self.news_url)
        stories = (
            Story.objects.filter(author=self.user, is_public=True)
            .order_by("-date_create")
            .all()
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "my_news.html")
        self.assertEqual(stories[0].title, "test_title_1")
        self.assertNotEqual(stories[0].title, "test_title_2")
        self.assertNotEqual(stories[0].is_public, False)


