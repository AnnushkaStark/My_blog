from django.test import TestCase

from stories.models import User, Story, Dislikes


class TestDislilkesModel(TestCase):
    """
    Тестирование модели реакции не нравится
    """

    def setUp(self):
        """
        Метод данных тест пользоватетеля
        и статьи и реакции  не нравиться
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

        self.dislike = Dislikes.objects.create(
            article=self.story, user=self.user
        )


    def test_dislikes_creation(self):
        """
        Проверка сохренения в модели реакции нравиться
        объекта класса Dislikes
        """
        self.assertTrue(isinstance(self.dislike, Dislikes))


    def test_models_fields(self):
        """
        Проверка данных содержащихся в полях модели
        """

        self.assertIsInstance(self.dislike.article, Story)
        self.assertIsInstance(self.dislike.user, User)
        

    def test_relationship(self):
        """
        Тест связи модели ползователя
        и модели статьи с моделью дизлайка
        """
        self.assertEqual(self.dislike.user, self.user)
        self.assertEqual(self.user, self.dislike.user)
        self.assertEqual(self.dislike.article, self.story)
        self.assertEqual(self.story, self.dislike.article)


