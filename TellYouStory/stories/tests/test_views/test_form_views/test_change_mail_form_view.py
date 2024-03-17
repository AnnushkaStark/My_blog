from django.test import TestCase, Client
from django.urls import reverse

from stories.models import User


class TestChangeUserMailFormView(TestCase):
    """
    Тестирование представление формы
    изменения электронной почты
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.change_mail_url = reverse("change_mail")
        self.user = User.objects.create_user(
            username="testus", email="mytest@mail.com", password="123testpassS@"
        )

        self.client.login(username="testus", password="123testpassS@")
        self.duplicate_user = User.objects.create_user(
            username="itsmyname", email="pochta@yandex.ru", password="Simple123!!pass"
        )

    def test_change_sucsess(self):
        """
        Тест успешное изменение элеткронной почты
        """
        data = {"old_mail": "mytest@mail.com", "new_mail": "my_new@gmail.ss"}
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.change_mail_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("settings_page"))
        user = User.objects.get(
            email=data["new_mail"]
        )  # Проверяем что почта  изменилась
        self.assertEqual(user.email, data["new_mail"])

    def test_change_failure(self):
        """
        Не успешное изменение почты
        """
        data = {"old_mail": "mytest@mail.com", "new_mail": "123@testpass"}
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.change_mail_url, data, follow=True)
        self.assertFalse(
            User.objects.filter(email="123@testpass").exists()
        )  # Проверяем что почта не изменилась
        self.assertRedirects(response, reverse("settings_page"))
        self.assertContains(response, "Ошибка изменения данных")

    def test_duplicate_mail(self):
        """
        Тестирование смены электронной
        почты на уже зарегистрированную
        """
        data = {"old_mail": "mytest@mail.com", "new_mail": "pochta@yandex.ru"}
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.change_mail_url, data, follow=True)
        self.assertFalse(
            User.objects.filter(email="123@testpass").exists()
        )  # Проверяем что почта не изменилась
        self.assertRedirects(response, reverse("settings_page"))
        self.assertContains(response, "Ошибка изменения данных")