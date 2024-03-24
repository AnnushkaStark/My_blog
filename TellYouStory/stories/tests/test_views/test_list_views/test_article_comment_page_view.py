from django.test import TestCase,Client
from django.urls import reverse

from stories.models import User, Story


class TestCommentPage(TestCase):
    """
    Тестирование доступности страницы 
    комментария
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
            "comment_page",
            kwargs={"article_id": self.article_id}
    )
    def test_comment_page(self):
        """
        Проверка доступности
        старницы комментария
        """
        self.client.login(
            username="testus", password="123testpassS@"
        )
        response = self.client.get(self.url)
        stories = Story.objects.filter(
             id=self.article_id, is_public=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "article_comment.html")
        self.assertEqual(stories[0].title, "test_title_1")

        