# Generated by Django 4.2.7 on 2024-02-17 10:09

from django.db import migrations, models
import stories.validators


class Migration(migrations.Migration):
    dependencies = [
        ("stories", "0005_likes_dislikes_comments_articlerewiews"),
    ]

    operations = [
        migrations.AlterField(
            model_name="biography",
            name="avatar",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="image/avatars/%Y",
                validators=[stories.validators.valid_file_size],
            ),
        ),
        migrations.AlterField(
            model_name="story",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="image/articles/%Y",
                validators=[stories.validators.valid_file_size],
            ),
        ),
    ]