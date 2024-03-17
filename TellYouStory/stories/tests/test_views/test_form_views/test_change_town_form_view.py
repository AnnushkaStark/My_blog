from django.test import TestCase, Client
from django.urls import reverse

from stories.models import User, Biography



class TestChangeTownFormView(TestCase):
    """
    Тестирвание представление формы
    изменения города пользователя
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.change_town_url = reverse("change_town")
        self.user = User.objects.create_user(
            username="testus", email="mytest@mail.com", password="123testpassS@"
        )
        self.client.login(username="testus", password="123testpassS@")

    def test_change_name_sucsess(self):
        """
        Успешная смена города
        """
        data = {
            "town": "Moscow",
        }
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.change_town_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("private_settings_page"))
        biography = Biography.objects.get(town=data["town"])
        self.assertEqual(biography.town, data["town"])
