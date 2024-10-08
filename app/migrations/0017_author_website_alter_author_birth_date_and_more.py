# Generated by Django 5.0.6 on 2024-07-05 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0016_alter_author_birth_date_alter_author_short_bio"),
    ]

    operations = [
        migrations.AddField(
            model_name="author",
            name="website",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="author",
            name="birth_date",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="author",
            name="short_bio",
            field=models.TextField(default="No bio available"),
        ),
    ]
