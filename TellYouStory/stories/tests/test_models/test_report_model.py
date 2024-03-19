from django.test import TestCase

from stories.models import Report, User, Story


class TestReportModel(TestCase):
    """
    Тестирование модели
    оставления жалобы
    на контент
    """
    def setUp(self):
        """
        создание тестовой
        жалобы, статьи
        и пользователя
        """
        self.user = User.objects.create(
            username="testuser",
            email="test@mail.com",
            password="my_password##&&7B",
        )

        self.story = Story.objects.create(
            title="testittle",
            topic="testtopic",
            image="test.jpg",
            content="somethingcontent",
            rank=1.0,
            like_counter=0,
            dislike_counter=0,
            comment_counter=0,
            views_counter=0,
            author=self.user,
        )

        self.report = Report.objects.create(
            title ="testtitle",
            text_report="testtext",
            author =self.user,
            content = self.story
        )


    def test_story_creation(self):
        """
        Проверка сохренения в модели объекта жалобы
        объекта жалобы
        """
        self.assertTrue(isinstance(self.report, Report))


    def test_models_fields(self):
        """
        Проверка данных содержащихся в полях модели
        """

        self.assertIsInstance(self.report.title, str)
        self.assertIsInstance(self.report.text_report, str)
        self.assertIsInstance(self.report.author, User)
        self.assertIsInstance(self.report.content, Story)

        
    def test_relationship(self):
        """
        Тест связи модели жалобы
        с моделью истории и ползователя
        """
        self.assertEqual(self.report.author, self.user)
        self.assertEqual(self.user, self.report.author)
        self.assertEqual(self.report.content, self.story)
        self.assertEqual(self.story, self.report.content)

