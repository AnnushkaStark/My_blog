from django.test import TestCase, Client
from django.urls import reverse

from stories.models import Story, User, ArticleRewiews


class TestOneStoryPage(TestCase):
    """
    Тестирование представления
    перехода на отделную статью
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username="testus",
            email="mytest@mail.com",
            password="123testpassS@"
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
        self.article_id = 1
        self.url = reverse(
            "one_story",
            kwargs={"article_id": self.article_id}
        )

    def test_one_story_page(self):
        """
        Проверка доступности
        старницы вывода
        oтдельной статьи
        """
        self.client.login(
            username="testus", password="123testpassS@"
        )
        response = self.client.get(self.url)
        story = Story.objects.get(id=self.article_id)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "one_story.html")
        self.assertEqual(story.title, "test_title_1")
        self.assertEqual(story.topic, "testopic_1")
        self.assertEqual(story.views_counter, 11)
        view = ArticleRewiews.objects.filter(
            article=self.article_1, user=self.user
        ).count()
        self.assertEqual(view, 1)


