from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Book(models.Model):
    isbn: models.CharField = models.CharField(max_length=13, unique=True)
    title: models.CharField = models.CharField(max_length=100)
    year: models.IntegerField = models.IntegerField()
    author: models.ForeignKey = models.ForeignKey(to="Author", on_delete=models.CASCADE)
    short_description: models.TextField = models.TextField()

    def __str__(self):
        return f"{self.title} - {self.author} - {self.year}"


class Author(models.Model):
    name: models.CharField = models.CharField(max_length=100)
    age: models.IntegerField = models.IntegerField()

    def __str__(self):
        return f"{self.name}"


class Review(models.Model):
    book: models.ForeignKey = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    added_by: models.ForeignKey = models.ForeignKey(to=User, on_delete=models.CASCADE)
    added_at: models.DateTimeField = models.DateTimeField(auto_now=True)
    comment: models.TextField = models.TextField()
    # If parent_review is null, that means that review is the parent/top level
    parent_review: models.ForeignKey = models.ForeignKey(
        to="Review", on_delete=models.CASCADE, null=True, blank=True
    )

    # TODO: Add upvote/down votes

    def __str__(self):
        return f"{self.comment} - {self.book} - {self.added_by} - {self.added_at}"


class UserProfile(models.Model):
    user: models.OneToOneField = models.OneToOneField(to=User, on_delete=models.CASCADE)
    age: models.PositiveIntegerField = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)], null=True, blank=True
    )
    country: models.CharField = models.CharField(max_length=100, null=True, blank=True)

    # TODO: add an image field and configure media files

    def __str__(self):
        return f"{self.user} - {self.age} - {self.country}"
