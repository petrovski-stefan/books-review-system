# Generated by Django 5.0.6 on 2024-06-22 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0010_alter_userprofile_age_alter_userprofile_country"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="short_description",
            field=models.TextField(null=True),
        ),
    ]
