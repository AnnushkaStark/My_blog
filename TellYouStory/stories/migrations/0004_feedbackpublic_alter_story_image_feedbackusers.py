# Generated by Django 4.2.7 on 2024-02-09 23:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("stories", "0003_story_rank"),
    ]

    operations = [
        migrations.CreateModel(
            name="FeedBackPublic",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=254)),
                ("topic", models.CharField(max_length=100)),
                ("text", models.TextField(max_length=3000)),
                ("date", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name_plural": "FeedBackPublic",
            },
        ),
        migrations.AlterField(
            model_name="story",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="image/articles/%Y"
            ),
        ),
        migrations.CreateModel(
            name="FeedBackUsers",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("topic", models.CharField(max_length=100)),
                ("description", models.TextField(max_length=3000)),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "FeedBackUsers",
            },
        ),
    ]