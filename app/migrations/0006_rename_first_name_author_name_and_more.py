# Generated by Django 5.0.6 on 2024-06-14 01:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0005_book_added_by_alter_book_author"),
    ]

    operations = [
        migrations.RenameField(
            model_name="author",
            old_name="first_name",
            new_name="name",
        ),
        migrations.RemoveField(
            model_name="author",
            name="last_name",
        ),
    ]
