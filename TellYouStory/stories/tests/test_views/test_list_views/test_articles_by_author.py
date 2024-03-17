from django.test import TestCase, Client
from django.urls import reverse

from stories.models import Story, User


class TestAuthorArticlesView(TestCase):
    """
    Тестирование представления
    отображения статей определенного
    автора с упорядочиванием
    по хронологии
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        и тест статей
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.user = User.objects.create_user(
            username="testus", email="mytest@mail.com", password="123testpassS@"
        )
        self.user_target = User.objects.create_user(
            username="testus_2", email="mytest@mail.ru", password="1234testpassS@"
        )

        self.article_1 = Story.objects.create(
            title="test_title_1",
            topic="testopic_1",
            image="test_image",
            author=self.user_target,
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

        self.author_id = 2
        self.author_article_url = reverse(
            "authors_articles", kwargs={"author_id": self.author_id}
        )

    