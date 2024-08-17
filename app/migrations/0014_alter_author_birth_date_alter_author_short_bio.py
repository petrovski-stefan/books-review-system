# Generated by Django 5.0.6 on 2024-06-29 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0013_rename_name_author_full_name_author_birth_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="author",
            name="birth_date",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="author",
            name="short_bio",
            field=models.TextField(),
        ),
    ]