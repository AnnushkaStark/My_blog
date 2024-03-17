from django.test import TestCase, Client
from django.urls import reverse

from stories.models import Story, User


class TestTimeArticlesView(TestCase):
    """
    Тестирование доступности страницы
    статей с упорядчиванеим по хронологии
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.time_articles_url = reverse("time_list_articles")
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
        self.article_2.rank = self.article_1.get_rank()
        self.article_2.save()

        self.article_3 = Story.objects.create(
            title="test_title_3",
            topic="testopic_3",
            image="test_image",
            author=self.user,
            like_counter=1,
            dislike_counter=0,
            comment_counter=1,
            views_counter=1,
        )
        self.article_3.rank = self.article_1.get_rank()
        self.article_3.save()

    def test_time_article_page(self):
        """
        Проверка доступности страницы
        с отображением статей по
        хронологии
        """
        self.client.login(username="tesuser", password="Test123#passS")
        response = self.client.get(self.time_articles_url)
        articles = Story.objects.filter(is_public=True).all().order_by("-date_create")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list_story_time.html")
        self.assertEqual(articles[0].title, "test_title_3")
        self.assertNotEqual(articles[0].is_public, False)
        self.assertEqual(articles[1].title, "test_title_2")
        self.assertNotEqual(articles[1].is_public, False)
        self.assertEqual(articles[2].title, "test_title_1")
        self.assertNotEqual(articles[2].is_public, False)


