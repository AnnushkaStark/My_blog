from django.test import TestCase

from stories.models import  FeedBackUsers, User

class TestFeedBackUserModel(TestCase):
    """
    Тестирование модели писем
    обратной связи от аутентифицированных
    пользователей
    """

    def setUp(self):
        """
        Метод данных тест пользоватетеля
        и тест письма обратной связи
        """
        self.user = User.objects.create(
            username="testuser",
            email="test@mail.com",
            password="my_password##&&7Q",
        )

        self.feedback = FeedBackUsers.objects.create(
            topic="test_topic", description="testtext", user=self.user
        )

    def test_feed_back_creation(self):
        """
        Проверка сохренения в модели объекта
        обращения от неаутентифицированного пользователя
        как объекта класса  FeedBackUsers
        """
        self.assertTrue(isinstance(self.feedback, FeedBackUsers))

    def test_models_fields(self):
        """
        Проверка данных содержащихся в полях модели
        """

        self.assertIsInstance(self.feedback.topic, str)
        self.assertIsInstance(self.feedback.description, str)
        self.assertIsInstance(self.feedback.user, User)

    def test_relationship(self):
        """
        Тест связи модели ползователя
          с моделью обращения
        """
        self.assertEqual(self.feedback.user, self.user)
        self.assertEqual(self.user, self.feedback.user)