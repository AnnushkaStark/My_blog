from django.test import TestCase

from stories.models import User


class TestUserModel(TestCase):
    """
    Teст модели пользователя
    """

    def setUp(self):
        """
        Метод данных тест пользоватетеля
        """
        self.user = User.objects.create(
            username="testuser",
            email="test@mail.com",
            password="my_password##&&7B",
        )

    def test_user_creation(self):
        """
        Проверка сохренения в модели объекта User
        """
        self.assertTrue(isinstance(self.user, User))

    def test_models_fields(self):
        """
        Проверка данных содержащихся в полях модели
        """

        self.assertIsInstance(self.user.username, str)
        self.assertIsInstance(self.user.email, str)
        self.assertIsInstance(self.user.password, str)
        self.assertIsInstance(self.user.is_verificate, bool)
        self.assertIsInstance(self.user.is_superuser, bool)
        self.assertIsInstance(self.user.is_active, bool)
