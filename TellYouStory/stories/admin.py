from django.contrib import admin
from .models import User

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
