# Generated by Django 4.2.7 on 2024-02-17 11:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stories", "0006_alter_biography_avatar_alter_story_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="story",
            name="comment_counter",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="story",
            name="dislike_counter",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="story",
            name="like_counter",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="story",
            name="views_counter",
            field=models.IntegerField(default=0),
        ),
    ]