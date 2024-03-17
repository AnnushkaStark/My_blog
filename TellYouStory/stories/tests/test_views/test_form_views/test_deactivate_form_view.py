from django.test import TestCase, Client
from django.urls import reverse

from stories.models import User


class TestDaectivateFormView(TestCase):
    """
    Тестирование представления формы деактивации
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.deactivate_url = reverse("deactivate_form")
        self.user = User.objects.create_user(
            username="testus", email="mytest@mail.com", password="123testpassS@"
        )
        self.client.login(username="testus", password="123testpassS@")

    def test_deactivate_sucsess(self):
        """
        Успешная деактивация
        """
        data = {
            "username": "testus",
            "email": "mytest@mail.com",
            "password": "123testpassS@",
            "password2": "123testpassS@",
        }
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.deactivate_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("index"))

    def test_deactivate_failure(self):
        """
        Не успешная деактивация не верный пароль
        """
        data = {
            "username": "testus",
            "email": "mytest@mail.com",
            "password": "12testpassS@",
            "password2": "123testpassS@",
        }
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.deactivate_url, data, follow=True)
        self.assertRedirects(response, reverse("deactivate_page"))
        self.assertContains(response, "Ошибка ввода данных")
