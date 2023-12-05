from django.contrib import admin
from .models import User, Articles


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Регистрация модели пользователя
    """
    list_display = ('username', 'email', 'password', 'biography', 'avatar')

@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    """
    Регистрация модели статей пользователя
    """
    list_display = ('create_date', 'title', 'content', 'image', 'deleted', 'author')