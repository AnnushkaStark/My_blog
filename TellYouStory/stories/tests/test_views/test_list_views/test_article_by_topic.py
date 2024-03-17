from django.test import TestCase, Client
from django.urls import reverse

from stories.models import Story, User


class TestTopicTimeView(TestCase):
    """
    Тестирование представления
    отображения статей
    по определенной тематике
    с упорядочиванием по хронологии
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        и тест статей
        """
        self.client = Client()
        self.topic = "testopic_1"
        self.url = reverse("user_page")
        self.time_topic_url = reverse(
            "article_topic_list", kwargs={"topic": self.topic}
        )
        self.user = User.objects.create_user(
            username="testus", email="mytest@mail.com", password="123testpassS@"
        )

        self.client.login(username="testus", password="123testpassS@")

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
            author=self.user,
            like_counter=5,
            dislike_counter=0,
            comment_counter=5,
            views_counter=5,
        )
        self.article_2.rank = self.article_2.get_rank()
        self.article_2.save()

        self.article_3 = Story.objects.create(
            title="test_title_3",
            topic="testopic_1",
            image="test_image",
            author=self.user,
            like_counter=1,
            dislike_counter=0,
            comment_counter=1,
            views_counter=1,
        )
        self.article_3.rank = self.article_3.get_rank()
        self.article_3.save()

    def test_topic_article_page(self):
        """
        Проверка доступности страницы
        с отображением статей по
        определенной тематике
        """
        self.client.login(username="tesuser", password="Test123#passS")
        response = self.client.get(self.time_topic_url)
        articles = (
            Story.objects.filter(
                topic=self.topic, is_public=True
            ).all().order_by("-date_create")
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "topic_time.html")
        self.assertEqual(articles[0].title, "test_title_3")
        self.assertNotEqual(articles[0].is_public, False)
        self.assertEqual(articles[1].title, "test_title_1")
        self.assertNotEqual(articles[1].is_public, False)
        self.assertNotEqual(articles[0].title, "test_title_2")
        self.assertNotEqual(articles[1].title, "test_title_2")
