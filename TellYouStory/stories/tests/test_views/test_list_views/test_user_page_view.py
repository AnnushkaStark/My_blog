from django.test import TestCase, Client
from django.urls import reverse

from stories.models import User, Biography

class TestUserPageView(TestCase):
    """
    Тестирование представления страницы пользователя
    """

    def setUp(self):
        """
        Создание тест пользователя
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username="tesuser",
            email="test@mail.ru",
            password="Test123#passS"
        )
        self.url = reverse("user_page")  # Страница user

    def test_user_page_without_bio(self):
        """
        Проверка доступности страницы user
        и того что при переходе на страницу если у пользователя
        нет биографии она корректно создается
        """
        self.client.login(username="tesuser", password="Test123#passS")
        response = self.client.get(self.url)
        self.biography = Biography(user=self.user)
        self.biography.save()
        biography = Biography.objects.filter(user=self.user).count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(biography, 1)
        self.assertTemplateUsed(response, "user.html")

    def test_user_page_with_bio(self):
        """
        Проверка доступности страницы и отображения биографии
        если она уже есть
        """
        self.biography = Biography(user=self.user, name="Vasya", town="test_town")
        self.biography.save()
        self.client.login(username="tesuser", password="Test123#passS")
        response = self.client.get(self.url)
        biography = Biography.objects.get(user=self.user)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, biography.name)
        self.assertContains(response, biography.town)
        self.assertTemplateUsed(response, "user.html")


