# Generated by Django 4.2.9 on 2024-01-28 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("post", "0004_rename_votes_tags_tags"),
    ]

    operations = [
        migrations.CreateModel(
            name="Comment",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("object_id", models.PositiveIntegerField()),
                ("author_object_id", models.PositiveIntegerField()),
                ("comment", models.TextField()),
                (
                    "author_content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="commented",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="replies",
                        to="post.comment",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="Reaction",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("object_id", models.PositiveIntegerField()),
                ("author_object_id", models.PositiveIntegerField()),
                (
                    "reaction",
                    models.CharField(
                        choices=[("L", "Love")], default="L", max_length=1
                    ),
                ),
                (
                    "author_content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reacted",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reactions",
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="Tag",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("object_id", models.PositiveIntegerField()),
                ("tag_object_id", models.PositiveIntegerField()),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tags",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "tag_content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tagged",
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="Vote",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("object_id", models.PositiveIntegerField()),
                ("author_object_id", models.PositiveIntegerField()),
                (
                    "vote",
                    models.CharField(
                        choices=[("U", "Up Vote"), ("D", "Down Vote")], max_length=1
                    ),
                ),
                (
                    "author_content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="voted",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="votes",
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="Vouch",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("object_id", models.PositiveIntegerField()),
                ("author_object_id", models.PositiveIntegerField()),
                (
                    "vouche",
                    models.CharField(
                        choices=[
                            ("L", "Low Vouch"),
                            ("M", "Medium Vouch"),
                            ("H", "High Vouch"),
                        ],
                        default="M",
                        max_length=1,
                    ),
                ),
                (
                    "author_content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="vouched",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="vouches",
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.RemoveField(model_name="reactions", name="content_type",),
        migrations.RemoveField(model_name="tags", name="content_type",),
        migrations.RemoveField(model_name="votes", name="content_type",),
        migrations.RemoveField(model_name="vouches", name="content_type",),
        migrations.AlterField(
            model_name="post",
            name="content_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="posted",
                to="contenttypes.contenttype",
            ),
        ),
        migrations.DeleteModel(name="Comments",),
        migrations.DeleteModel(name="Reactions",),
        migrations.DeleteModel(name="Tags",),
        migrations.DeleteModel(name="Votes",),
        migrations.DeleteModel(name="Vouches",),
    ]
