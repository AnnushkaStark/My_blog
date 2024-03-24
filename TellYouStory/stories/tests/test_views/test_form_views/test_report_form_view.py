from django.test import TestCase , Client
from django.urls import reverse

from stories.models import User, Report, Story


class TestReportFormVies(TestCase):
    """
    Тестирование представления
    формы жалобы
    """
    def setUp(self):
        """
        Cоздание тест пользователя
        """
        self.client = Client()
        self.url = reverse("user_page")
        self.user = User.objects.create_user(
            username="testus", email="mytest@mail.com", password="123testpassS@"
        )
        self.client.login(username="testus", password="123testpassS@")
        self.article_1 = Story.objects.create(
            title="test_title_1",
            topic="testopic_1",
            image="test_image",
            author=self.user,
            like_counter=10,
            dislike_counter=0,
            comment_counter=10,
            views_counter=10,
        )
        self.article_1.rank = self.article_1.get_rank()
        self.article_1.save()
        self.target_article = 1
        self.report_url = reverse(
            "report_form",
            kwargs={"article_id": self.target_article}
        )
    def test_send_report_success(self):
        """
        Успешная отправка
        обратной жалобы
        """
        data = {
            "title":"testtitle",
            "text_report":"test_text",
            }
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.report_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response, reverse("one_story", kwargs={"article_id": self.target_article})
        )
        self.assertContains(response, "Обращение отправлено.")

    def test_send_repor_invalid_title(self):
        """
        Тест попытка отправки формы обратной
        связи с невалидной формой
        не наполнен заголовок
        """
        data = {
            "title":"",
            "text_report":"test_text",
            }
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.report_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response, reverse("report_page", kwargs={"article_id": self.target_article})
        )
        self.assertContains(response, "Обращение не прошло модерацию")


    def test_send_report_invalid_text_repot(self):
        """
        Попытка отправи не валидной формы
        не заполнен текст обращения
        """
        data = {
            "title":"test_title",
            "text_report":"",
            }
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.report_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response, reverse("report_page", kwargs={"article_id": self.target_article})
        )
        self.assertContains(response, "Обращение не прошло модерацию")

    def test_send_report_ban_title_repot(self):
        """
        Попытка отправки не валидной формы
        нецензурное слово в заголовке
        """
        data = {
            "title":"гонорея",
            "text_report":"тесттест",
            }
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.report_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response, reverse("report_page", kwargs={"article_id": self.target_article})
        )
        self.assertContains(response, "Обращение не прошло модерацию")


    def test_send_report_ban_text_repot(self):
        """
        Попытка отправи не валидной формы
        нецензурное слово в теме писма
        """
        data = {
            "title":"testtest",
            "text_report":"гонорея",
            }
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.report_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response, reverse("report_page", kwargs={"article_id": self.target_article})
        )
        self.assertContains(response, "Обращение не прошло модерацию")

    def test_send_blank_form(self):
        """
        Попытка отправки не заполненной формы
        """
        data = {
            "title":"",
            "text_report":"",
            }
        response = self.client.get(reverse("user_page"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.report_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response, reverse("report_page", kwargs={"article_id": self.target_article})
        )
        self.assertContains(response, "Обращение не прошло модерацию")

