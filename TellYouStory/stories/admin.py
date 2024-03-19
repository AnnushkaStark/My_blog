from django.contrib import admin
from .models import (
    User,
    Biography,
    Story,
    FeedBackPublic,
    FeedBackUsers,
    Likes,
    Dislikes,
    ArticleRewiews,
    Comments,
    Report,
)



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Регистрация модели пользователя
    """

    list_display = (
        "username",
        "email",
        "password",
        "is_verificate",
        "is_superuser",
        "is_active",
    )

    ordering =["username"]
    list_filter =["username"]
    search_fields = ["email","username"]
    search_help_text = 'Поиск по полю email или username'


@admin.register(Biography)
class BiographyAdmin(admin.ModelAdmin):
    """
    Регитсрация модели биографии пользователя
    """

    list_display = ("name", "town", "birth_date", "link", "avatar", "bio", "user")

    ordering =["name"]
    list_filter =["name"]
    search_fields = ["name","tow"]
    search_help_text = "Поиск по полю name или town"


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    """
    Регистрация модели истории
    """

    list_display = (
        "title",
        "topic",
        "image",
        "content",
        "date_create",
        "date_update",
        "is_public",
        "rank",
        "like_counter",
        "dislike_counter",
        "comment_counter",
        "views_counter",
        "author",
    )

    ordering =["topic"]
    list_filter =["topic"]
    search_fields = ["title","topic"]
    search_help_text = "Поиск по полю title или topic"


@admin.register(FeedBackUsers)
class FeedBackUsersAdmin(admin.ModelAdmin):
    """
    Регистрация модели писем обратной
    связи от зарегистрированных пользователей
    """

    list_display = ("topic", "description", "date", "user")

    ordering =["topic"]
    list_filter =["topic"]
    search_fields = ["topic"]
    search_help_text = "Поиск по полю  topic"


@admin.register(FeedBackPublic)
class FeedBackPublicAdmin(admin.ModelAdmin):
    """
    Регистрация модели писем обратной
    связи от не зарегистрированных
    пользователей
    """

    list_display = ("name", "email", "topic", "text", "date")

    ordering =["topic"]
    list_filter =["topic"]
    search_fields = ["topic","name","email"]
    search_help_text = "Поиск по полю  topic, name, email"


@admin.register(Likes)
class AdminLikes(admin.ModelAdmin):
    """
    Регистрация модели реакций нравиться
    """

    list_display = ("article","user")


@admin.register(Dislikes)
class AdminDislikes(admin.ModelAdmin):
    """
    Регистрация модели реакций 
    не нравиться
    """

    list_display = ("article","user")



@admin.register(ArticleRewiews)
class AdminrticleRewiews(admin.ModelAdmin):
    """
    Регистрация модели реакций 
    не нравиться
    """

    list_display = ("article","user")


@admin.register(Comments)
class AdminComments(admin.ModelAdmin):
    """
    Регистрация модели 
    комментариев 
    """
    list_display = ("text","date", "article","user")
    list_filter =["text","article"]


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """
    Регистрация модели жалобы
    """
    list_display =(
        "title",
        "text_report",
        "date",
        "author",
        "content"
    )

    list_filter =["date","content"]
    ordering =["date"]
    search_fields = ["title"]
    search_help_text = "Поиск по полю  title"