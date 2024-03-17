from django.test import TestCase
from django.db.models.fields.files import ImageFieldFile

from stories.models import User, Biography

class TestBiographyModel(TestCase):
    """
    Тестирование  модели биографии пользователя
    """

    def setUp(self):
        """
        Метод данных тест пользоватетеля
        и тест биографии
        """
        self.user = User.objects.create(
            username="testuser",
            email="test@mail.com",
            password="my_password##&&7Q",
        )

        self.bio = Biography.objects.create(
            name="test",
            town="TestCity",
            birth_date="2024-01-07",
            link="https://stepik.org/lesson/1098495/step/5?unit=1109364",
            avatar="test.jpg",
            bio="my_long_long_bio",
            user=self.user,
        )


    def test_bio_creation(self):
        """
        Проверка сохренения в модели объекта биографии
        объекта биография
        """
        self.assertTrue(isinstance(self.bio, Biography))



    def test_models_fields(self):
        """
        Проверка данных содержащихся в полях модели
        """

        self.assertIsInstance(self.bio.name, str)
        self.assertIsInstance(self.bio.town, str)
        self.assertIsInstance(self.bio.birth_date, str)
        self.assertIsInstance(self.bio.link, str)
        self.assertIsInstance(self.bio.avatar, ImageFieldFile)
        self.assertIsInstance(self.bio.bio, str)
        self.assertIsInstance(self.bio.user, User)

        

    def test_relationship(self):
        """
        Тест связи модели ползователя
          с моделью биографии
        """
        self.assertEqual(self.bio.user, self.user)
        self.assertEqual(self.user, self.bio.user)
