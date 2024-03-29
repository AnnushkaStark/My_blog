from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import valid_file_size

# Create your models here.


class User(AbstractUser):
    """
    Модель пользователя сайта
    """

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    is_verificate = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        """
        Отображение полей в админке
        """
        return f"{self.username} {self.email} {self.password}  {self.is_verificate}  {self.is_superuser} {self.is_active}"


class Biography(models.Model):
    """
    Модель биографии пользователя
    заполнение личных данных профиля
    """

    name = models.CharField(max_length=100, blank=True, null=True)
    town = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    avatar = models.ImageField(
        upload_to="image/avatars/%Y",
        blank=True,
        null=True,
        validators=[valid_file_size],
    )
    bio = models.TextField(max_length=2000, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        verbose_name_plural = "Biographys"

    def __str__(self):
        return f"{self.name} {self.town} {self.birth_date} {self.link} {self.avatar} {self.bio} {self.user.username}"


class Story(models.Model):
    """
    Модель поста (истории)
    """

    title = models.CharField(max_length=100)  # Заголовок
    topic = models.CharField(max_length=100)  # Тема
    image = models.ImageField(
        upload_to="image/articles/%Y",
        blank=True,
        null=True,
        validators=[valid_file_size],
    )
    content = models.TextField(max_length=5000, blank=True, null=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)
    rank = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    like_counter = models.IntegerField(default=0)
    dislike_counter = models.IntegerField(default=0)
    comment_counter = models.IntegerField(default=0)
    views_counter = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Stories"

    def __str__(self):
        return f"{self.title} {self.topic} {self.image} {self.content} {self.date_create} {self.date_update} {self.is_public} {self.rank} {self.like_counter} {self.dislike_counter} {self.comment_counter} {self.views_counter} {self.author}"

    def get_rank(self):
        """
        Метод получения ранга статьи
        """
        self.rank = (
            self.like_counter * 0.3
            + self.comment_counter * 0.3
            + self.views_counter * 0.2
        ) - self.dislike_counter * 0.3
        return self.rank


class FeedBackUsers(models.Model):
    """
    Модель сохранени писем по обратной связи
    от зарегистрированных пользователей сайта
    """

    topic = models.CharField(max_length=100)
    description = models.TextField(max_length=3000)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "FeedBackUsers"

    def __str__(self):
        return f"{self.topic} {self.description} {self.date} {self.user}"


class FeedBackPublic(models.Model):
    """
    Модель сохранения писем по
    обратной связи от пользователей
    не зарегистрированных на сайте
    """

    name = models.CharField(max_length=50)
    email = models.EmailField()
    topic = models.CharField(max_length=100)
    text = models.TextField(max_length=3000)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "FeedBackPublic"

    def __str__(self):
        return f"{self.name} {self.email} {self.topic} {self.text} {self.date}"


class Likes(models.Model):
    """
    Модель реакций нравиться
    """

    article = models.ForeignKey(Story, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Likes"

    def __str__(self):
        return f"{self.article} {self.user}"


class Dislikes(models.Model):
    """
    Модель реакций не нравится
    """

    article = models.ForeignKey(Story, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Dislikes"

    def __str__(self):
        return f"{self.article} {self.user}"


class ArticleRewiews(models.Model):
    """
    Модель реакции просмотр
    """

    article = models.ForeignKey(Story, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "ArticleRewiews"

    def __str__(self):
        return f"{self.article} {self.user}"


class Comments(models.Model):
    """
    Модель комментария
    """

    text = models.TextField(max_length=3000)
    date = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Story, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"{self.text} {self.date} {self.article} {self.user}"
    

class Report(models.Model):
    """
    Модель  жалобы
    """
    title = models.CharField(max_length=100)
    text_report = models.TextField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Story, on_delete=models.CASCADE)

    def __str__(self):

        return f"{self.title} {self.text_report} {self.date} {self.author} {self.content}"
