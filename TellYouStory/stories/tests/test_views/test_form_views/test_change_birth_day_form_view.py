from django.test import TestCase, Client
from django.urls import reverse

from stories.models import User, Biography



class TestChangeBirthDateFormView(TestCase):
    """
    Тестирование формы представления
    изменения даты рождения пользователя
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.change_birth_date_url = reverse("change_birth_date")
        self.user = User.objects.create_user(
            username="testus",
            email="mytest@mail.com",
            password="123testpassS@"
        )
        self.client.login(username="testus", password="123testpassS@")

    def test_change_birth_date_sucsess(self):
        """
        Успешная смена даты рождения
        """
        data = {
            "birth_date": "2024-09-01",
        }
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.change_birth_date_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("private_settings_page"))
        biography = Biography.objects.filter(birth_date=data["birth_date"]).count()
        self.assertEqual(biography, 1)

    def test_change_birth_date_failure(self):
        """
        Не успешное изменение даты рождения
        """
        data = {
            "birth_date": "1234567",
        }
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.change_birth_date_url, data, follow=True)
        self.assertRedirects(response, reverse("private_settings_page"))
        self.assertContains(response, "Ошибка ввода данных")

