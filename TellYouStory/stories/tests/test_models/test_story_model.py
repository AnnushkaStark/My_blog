from django.test import TestCase
from django.db.models.fields.files import ImageFieldFile

from stories.models import Story, User


class TestStoryModel(TestCase):
    """
    Тестирование  модели истории (статьи) пользователя
    """

    def setUp(self):
        """
        Метод данных тест пользоватетеля
        и тест истории
        """
        self.user = User.objects.create(
            username="testuser",
            email="test@mail.com",
            password="my_password##&&7Q",
        )

        self.story = Story.objects.create(
            title="testittle",
            topic="testtopic",
            image="test.jpg",
            content="somethingcontent",
            rank=1.0,
            like_counter=0,
            dislike_counter=0,
            comment_counter=0,
            views_counter=0,
            author=self.user,
        )

    def test_story_creation(self):
        """
        Проверка сохренения в модели объекта истории
        объекта истории
        """
        self.assertTrue(isinstance(self.story, Story))

    def test_models_fields(self):
        """
        Проверка данных содержащихся в полях модели
        """

        self.assertIsInstance(self.story.title, str)
        self.assertIsInstance(self.story.topic, str)
        self.assertIsInstance(self.story.image, ImageFieldFile)
        self.assertIsInstance(self.story.content, str)
        self.assertIsInstance(self.story.is_public, bool)
        self.assertIsInstance(self.story.rank, float)
        self.assertIsInstance(self.story.like_counter, int)
        self.assertIsInstance(self.story.dislike_counter, int)
        self.assertIsInstance(self.story.comment_counter, int)
        self.assertIsInstance(self.story.views_counter, int)
        self.assertIsInstance(self.story.author, User)

    def test_relationship(self):
        """
        Тест связи модели ползователя
          с моделью истории
        """
        self.assertEqual(self.story.author, self.user)
        self.assertEqual(self.user, self.story.author)
