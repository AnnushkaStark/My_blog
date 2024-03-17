from django.test import TestCase, Client
from django.urls import reverse

from stories.models import Story, User


class TestDeleteStoryView(TestCase):
    """
    Тестирование эндпойнта
    удаление истории
    """

    def setUp(self):
        """
        Создание тест пользователя
        и тест статьи
        """
        self.target_article = 1
        self.del_url = reverse(
            "del_story",
            kwargs={"article_id": self.target_article}
        )
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

        self.article_2 = Story.objects.create(
            title="test_title_2",
            topic="testopic_2",
            image="test_image",
            author=self.user,
            like_counter=10,
            dislike_counter=0,
            comment_counter=10,
            views_counter=10,
        )
        self.article_2.rank = self.article_2.get_rank()
        self.article_2.save()

    def test_delete_story_sucsess(self):
        """
        Тестирование удаления истории
        """
        self.client.login(
            username="testus", password="123testpassS@"
        )
        response = self.client.post(self.del_url, follow=True)
        stories = Story.objects.get(
            author=self.user, id=self.target_article
        )
        stories.is_public = False
        stories.save()
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("my_stories"))
        self.assertContains(response, "Статья успешно удалена")
        deleted_article = Story.objects.get(
            author=self.user, id=self.target_article
        )
        self.assertEqual(deleted_article.is_public, False)


