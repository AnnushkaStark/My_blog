from django.test import TestCase, Client
from django.urls import reverse

from stories.models import User, Story, Likes, Dislikes


class TestLikeStoryView(TestCase):
    """
    Тестирование представлние
    проставления раекции нравиться
    """
    def setUp(self):
        """
        Cоздание тест пользователя
        и тест статьи
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
            dislike_counter= 0,
            comment_counter=10,
            views_counter=10,
        )
        self.article_id = 1
        self.like_url = reverse(
            "like_article",
            kwargs={"article_id": self.article_id}
        )
    def test_like_story(self):
        """
        тест успешного проставления
        реакции нравится
        """
        self.client.login(
            username="testus", password="123testpassS@"
        )
        expected_url = reverse(
            "one_story", kwargs={"article_id": self.article_id}
        )
        response = self.client.post(self.like_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, expected_url)
        like = Likes.objects.filter(
            article=self.article_1,
            user=self.user
        ).count()
        self.assertEqual(1,like)
        story = Story.objects.get(id=self.article_id)
        self.assertEqual(story.like_counter,11)

    def test_like_story_duplicate(self):
        """
        Попытка поставить лайк на статью
        второй раз 
        """
        like = Likes.objects.create(
            article=self.article_1,
            user=self.user)
        self.client.login(
            username="testus", password="123testpassS@"
        )
        expected_url = reverse(
            "one_story", kwargs={"article_id": self.article_id}
        )
        response = self.client.post(self.like_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, expected_url)
        like = Likes.objects.filter(
            article=self.article_1,
            user=self.user
        ).count()
        self.assertEqual(1,like)
        story = Story.objects.get(id=self.article_id)
        self.assertEqual(story.like_counter,10)

    def test_like_with_dislike(self):
        """
        Тест удаление дизлайка статеье 
        от пользователя при проставлении
        им лайка 
        """
        dislike = Dislikes.objects.create(
            article=self.article_1,
            user=self.user)
        self.client.login(
            username="testus", password="123testpassS@"
        )
        expected_url = reverse(
            "one_story", kwargs={"article_id": self.article_id}
        )
        response = self.client.post(self.like_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, expected_url)
        like = Likes.objects.filter(
            article=self.article_1,
            user=self.user
        ).count()
        self.assertEqual(1,like)
        dislike = Dislikes.objects.filter(
            article=self.article_1,
            user=self.user
        ).count()
        self.assertEqual(0,dislike)
        story = Story.objects.get(id=self.article_id)
        self.assertEqual(story.like_counter,11)
        self.assertEqual(story.dislike_counter,0)