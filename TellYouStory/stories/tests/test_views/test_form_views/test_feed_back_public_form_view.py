from django.test import TestCase, Client
from django.urls import reverse

from  stories.models import FeedBackPublic

class TestFeedbackPublicFormView(TestCase):
    """
    Тестирование представления формы
    оствления обратной связи
    для не аутентифицированного пользователя
    """

    def setUp(self):
        """
        Создание тест пользователя
        """
        self.client = Client()
        self.url = reverse("feed_back_public")

    def test_send_feedback_sucsess(self):
        """
        Успешная отправка обратной связи
        """
        data = {
            "name": "test_name",
            "email": "test@mail.com",
            "topic": "tast_topic",
            "text": "test_text",
        }

        response = self.client.get(reverse("feed_back_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("feed_back_page"))
        feedback = FeedBackPublic.objects.get(name=data["name"])
        self.assertEqual(feedback.name, "test_name")
        self.assertEqual(feedback.email, "test@mail.com")
        self.assertEqual(feedback.topic, "tast_topic")
        self.assertEqual(feedback.text, "test_text")

    def test_send_feedback_failure(self):
        """
        Не успешная отправка обратной
        связи
        """
        data = {
            "name": "",
            "email": "test_topic",
            "topic": "tast.jpg",
            "text": "test_text",
        }

        response = self.client.get(reverse("feed_back_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response, reverse("feed_back_page"))
        self.assertContains(response, "Обращение не прошло модерацию")
