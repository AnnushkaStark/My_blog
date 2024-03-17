from django.test import TestCase

from stories.models import User, Story, ArticleRewiews


class TestArticlereviewsModel(TestCase):
    """
    Тестирование модели реакции просмтр
    """

    def setUp(self):
        """
        Метод данных тест пользоватетеля
        и статьи и реакции просмотр
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

        self.review = ArticleRewiews.objects.create(
            article=self.story, user=self.user
        )

    def test_reviews_creation(self):
        """
        Проверка сохренения в модели реакции просмотр
        объекта класса ArticleRewiews
        """
        self.assertTrue(isinstance(self.review, ArticleRewiews))

    def test_models_fields(self):
        """
        Проверка данных содержащихся в полях модели
        """

        self.assertIsInstance(self.review.article, Story)
        self.assertIsInstance(self.review.user, User)

    def test_relationship(self):
        """
        Тест связи модели ползователя
        и модели статьи с моделью просмотра
        """
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.user, self.review.user)
        self.assertEqual(self.review.article, self.story)
        self.assertEqual(self.story, self.review.article)
