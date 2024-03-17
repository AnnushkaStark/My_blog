from django.test import TestCase, Client
from django.urls import reverse

from stories.models import User, Biography


class TestChangeNameFormView(TestCase):
    """
    Тестирование представления формы
    изменения имени пользователя
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.change_name_url = reverse("change_name")
        self.user = User.objects.create_user(
            username="testus", email="mytest@mail.com", password="123testpassS@"
        )
        self.client.login(username="testus", password="123testpassS@")

    def test_change_name_sucsess(self):
        """
        Успешная смена имени
        """
        data = {
            "name": "test",
        }
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.change_name_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("private_settings_page"))
        biography = Biography.objects.get(name=data["name"])
        self.assertEqual(biography.name, data["name"])