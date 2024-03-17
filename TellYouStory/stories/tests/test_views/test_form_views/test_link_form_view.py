from django.test import TestCase, Client
from django.urls import reverse

from stories.models import User, Biography


class TestChangeLinkFormView(TestCase):
    """
    Тестирование представления формы изменения ссылки
    на соц сеть или бусти в профиле пользователя
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.change_link_url = reverse("link_change")
        self.user = User.objects.create_user(
            username="testus",
            email="mytest@mail.com",
            password="123testpassS@"
        )
        self.client.login(username="testus", password="123testpassS@")

    def test_change_link_sucsess(self):
        """
        Успешное изменение ссылки на соц сеть
        или бусти в профиле пользователя
        """
        data = {
            "link": "",  # Поле может быть пустым
        }
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.change_link_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("private_settings_page"))
        biography = Biography.objects.get(link=data["link"])
        self.assertEqual(biography.link, data["link"])

    def test_change_link_failure(self):
        """
        Не успешное изменение ссылки на соц сеть
        или бусти в профиле пользователя

        """
        data = {
            "link": "1234567",
        }
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.change_link_url, data, follow=True)
        self.assertRedirects(response, reverse("private_settings_page"))
        self.assertContains(response, "Ошибка ввода данных")
