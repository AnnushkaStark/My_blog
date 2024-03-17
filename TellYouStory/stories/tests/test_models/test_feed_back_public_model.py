from django.test import TestCase

from stories.models import FeedBackPublic


class TestFeedBackPublicModel(TestCase):
    """
    Тестирование модели
    писем обратной связи
    от не авторизованных
    пользователей
    """

    def setUp(self):
        """
        создание тестового
        обращения
        """
        self.feedback = FeedBackPublic.objects.create(
            name="testname",
            email="test@mail.ru",
            topic="test_topic",
            text="testtext"
        )

    def test_feed_back_creation(self):
        """
        Проверка сохренения в модели объекта
        обращения от неаутентифицированного пользователя
        как объекта класса  FeedBackPublic
        """
        self.assertTrue(isinstance(self.feedback, FeedBackPublic))

    def test_models_fields(self):
        """
        Проверка данных содержащихся в полях модели
        """

        self.assertIsInstance(self.feedback.name, str)
        self.assertIsInstance(self.feedback.email, str)
        self.assertIsInstance(self.feedback.topic, str)
        self.assertIsInstance(self.feedback.text, str)
