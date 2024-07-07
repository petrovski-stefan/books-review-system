# Generated by Django 5.0.6 on 2024-07-06 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0017_author_website_alter_author_birth_date_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Genre",
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
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField()),
            ],
        ),
    ]
