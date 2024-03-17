from django.test import TestCase, Client
from django.urls import reverse

from stories.models import User, Biography


class TestAuthorInfoView(TestCase):
    """
    Тестирование представления
    вывода информации об определенном авторе
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username="testus", email="mytest@mail.com", password="123testpassS@"
        )
        self.author_id = 1
        self.url = reverse("author_info", kwargs={"author_id": self.author_id})

        self.bio = Biography.objects.create(
            name="test",
            town="TestCity",
            birth_date="2024-01-07",
            link="https://stepik.org/lesson/1098495/step/5?unit=1109364",
            avatar="test.jpg",
            bio="my_long_long_bio",
            user=self.user,
        )

    def test_author_article_page(self):
        """
        Проверка доступности страницы
        с отображением информации
        об авторе
        """
        self.client.login(username="testus", password="123testpassS@")
        response = self.client.get(self.url)
        biography = Biography.objects.get(user_id=self.author_id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, biography.name)
        self.assertContains(response, biography.town)
        self.assertContains(response, biography.link)
        self.assertContains(response, biography.avatar)
        self.assertContains(response, biography.bio)


