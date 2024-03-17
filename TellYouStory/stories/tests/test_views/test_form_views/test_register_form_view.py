from django.test import TestCase , Client
from django.urls import reverse

from stories.models import User


class TestUserRegistrationFormView(TestCase):
    """
    Тестирование предствления формы регистрации пользоватея
    """

    def setUp(self):
        """
        Создание тест пользователя
        """
        self.client = Client()
        self.url = reverse("register_form")
        self.data = {
            "username": "tesuser",
            "email": "test@mail.com",
            "password": "testpassword#!@T1",
            "password2": "testpassword#!@T1",
        }

    def test_register_form_view_sucsess(self):
        """
        Проверка успешной регистрации
        """
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login_page"))
        user = User.objects.get(username=self.data["username"])
        self.assertEqual(user.email, self.data["email"])
        self.assertTrue(user.check_password(self.data["password"]))

    def test_register_form_view_failure(self):
        """
        Тестирование регистрации при не валидной форме
        """
        invalid_data = self.data.copy()
        invalid_data["password2"] = "wrongpassword"
        response = self.client.post(self.url, data=invalid_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("register"))
        self.assertContains(response, "Ошибка ввода данных")
        self.assertFalse(User.objects.filter(username="tesuser").exists())

    def test_blank_data(self):
        """
        Тестирование попытки регистрации
        c  не валидной формой ( пустой юзернейм)
        """
        blank_data = self.data.copy()
        blank_data["username"] = ""
        response = self.client.post(self.url, data=blank_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("register"))
        self.assertContains(response, "Ошибка ввода данных")

