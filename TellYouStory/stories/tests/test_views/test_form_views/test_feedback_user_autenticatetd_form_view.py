from django.test import TestCase, Client
from django.urls import reverse

from stories.models import User, FeedBackUsers


class TestFeeedbackPublicFormView(TestCase):
    """
    Тестирование представления
    формы отправки обратной связи
    для аутентифицированного
    пользователя
    """

    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.send_feedback_url = reverse("feed_back_user")
        self.user = User.objects.create_user(
            username="testus", email="mytest@mail.com", password="123testpassS@"
        )
        self.client.login(username="testus", password="123testpassS@")

    def test_send_feedback_sucsess(self):
        """
        Успешная отправка
        обратной связи
        """
        data = {
            "topic": "test_title",
            "description": "test_topic",
        }

        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.send_feedback_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("feed_back_page"))
        feedback = FeedBackUsers.objects.get(user=self.user)
        self.assertEqual(feedback.user, self.user)

    def test_send_feedback_failure(self):
        """
        Не успешная отправка
        обратной связи
        """
        data = {
            "topic": "",
            "description": "test_topic",
        }

        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.send_feedback_url, data, follow=True)
        self.assertRedirects(response, reverse("feed_back_page"))
        self.assertContains(response, "Обращение не прошло модерацию")

