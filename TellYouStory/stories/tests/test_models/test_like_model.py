from django.test import TestCase
from stories.models import User, Story, Likes

class TestLilkesModel(TestCase):
    """
    Тестирование модели реакции нравится
    """

    def setUp(self):
        """
        Метод данных тест пользоватетеля
        и статьи и реакции нравиться
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
            rank=0.0,
            author=self.user,
        )

        self.like = Likes.objects.create(article=self.story, user=self.user)

    def test_likes_creation(self):
        """
        Проверка сохренения в модели реакции нравиться
        объекта класса Likes
        """
        self.assertTrue(isinstance(self.like, Likes))

    def test_models_fields(self):
        """
        Проверка данных содержащихся в полях модели
        """

        self.assertIsInstance(self.like.article, Story)
        self.assertIsInstance(self.like.user, User)

    def test_relationship(self):
        """
        Тест связи модели ползователя
        и модели статьи с моделью лайка
        """
        self.assertEqual(self.like.user, self.user)
        self.assertEqual(self.user, self.like.user)
        self.assertEqual(self.like.article, self.story)
        self.assertEqual(self.story, self.like.article)
