from django.test import TestCase, Client
from django.urls import reverse

from stories.models import User, Biography


class TestChangeBiographyFormView(TestCase):
    """
    Тестирование представления формы
    изменения биографии пользователя
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.change_bio_url = reverse("bio_change")
        self.user = User.objects.create_user(
            username="testus",
            email="mytest@mail.com",
            password="123testpass@Q"
        )
        self.client.login(
            username="testus", password="123testpass@Q"
        )

    def test_change_name_sucsess(self):
        """
        Успешная смена биографии
        """
        data = {
            "bio": "bla-bla-bla",
        }
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.change_bio_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("private_settings_page"))
        biography = Biography.objects.get(bio=data["bio"])
        self.assertEqual(biography.bio, data["bio"])

