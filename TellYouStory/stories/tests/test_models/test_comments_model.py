from django.test import TestCase

from stories.models import User, Story, Comments



class TestCommentsModel(TestCase):
    """
    Тестирование модели коментария
    """

    def setUp(self):
        """
        Метод данных тест пользоватетеля
        и статьи и комментраия
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

        self.comment = Comments.objects.create(
            text="test_text", article=self.story, user=self.user
        )

    
    def test_comment_creation(self):
        """
        Проверка сохренения в модели комментария
        объекта класса Cоmments
        """
        self.assertTrue(isinstance(self.comment, Comments))

   
    def test_models_fields(self):
        """
        Проверка данных содержащихся в полях модели
        """

        self.assertIsInstance(self.comment.article, Story)
        self.assertIsInstance(self.comment.user, User)
        self.assertIsInstance(self.comment.text, str)

    
    def test_relationship(self):
        """
        Тест связи модели ползователя
        и модели статьи с моделью комментария
        """
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.user, self.comment.user)
        self.assertEqual(self.comment.article, self.story)
        self.assertEqual(self.story, self.comment.article)

