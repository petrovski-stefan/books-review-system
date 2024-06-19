from django.contrib import admin
from .models import Book, Author, Review, UserProfile

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Review)
admin.site.register(UserProfile)
