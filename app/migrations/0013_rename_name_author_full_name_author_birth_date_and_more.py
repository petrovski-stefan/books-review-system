# Generated by Django 5.0.6 on 2024-06-29 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0012_alter_book_short_description"),
    ]

    operations = [
        migrations.RenameField(
            model_name="author",
            old_name="name",
            new_name="full_name",
        ),
        migrations.AddField(
            model_name="author",
            name="birth_date",
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name="author",
            name="death_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="author",
            name="short_bio",
            field=models.TextField(null=True),
        ),
    ]
