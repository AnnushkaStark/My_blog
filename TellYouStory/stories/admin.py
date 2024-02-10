from django.contrib import admin
from .models import User, Biography, Story, FeedBackPublic, FeedBackUsers

# Register your models here.


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


@admin.register(Biography)
class BiographyAdmin(admin.ModelAdmin):
    """
    Регитсрация модели биографии пользователя
    """

    list_display = ("name", "town", "birth_date", "link", "avatar", "bio", "user")


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
        "author",
    )


@admin.register(FeedBackUsers)
class FeedBackUsersAdmin(admin.ModelAdmin):
    """
    Регистрация модели писем обратной
    связи от зарегистрированных пользователей
    """

    list_display = ("topic", "description", "date", "user")


@admin.register(FeedBackPublic)
class FeedBackPublicAdmin(admin.ModelAdmin):
    """
    Регистрация модели писем обратной
    связи от не зарегистрированных
    пользователей
    """

    list_display = ("name", "email", "topic", "text", "date")
