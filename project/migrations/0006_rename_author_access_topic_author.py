# Generated by Django 4.2.8 on 2024-01-07 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0005_alter_topic_author_access"),
    ]

    operations = [
        migrations.RenameField(
            model_name="topic", old_name="author_access", new_name="author",
        ),
    ]
