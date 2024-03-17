from django.test import TestCase , Client
from django.urls import reverse

from stories.models import User


class TestLoginFormView(TestCase):
    """
    Тестирование  представления формы login
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.login_url = reverse("login_form")
        self.user = User.objects.create_user(
            username="testus", email="mytest@mail.com", password="123testpassS@"
        )

    def test_login_form_view_sucsess(self):
        """
        Успешный вход в систему
        """
        data = {"username": "testus", "password": "123testpassS@"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user_page"))

    def test_login_form_view_failure(self):
        """
        Не успешный вход в систеу
        """
        data = {"username": "testus", "password": "123testS"}

        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login_page"))
