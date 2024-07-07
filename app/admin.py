from django.contrib import admin
from .models import Book, Author, Review, UserProfile, Genre


class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Book)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Author)
admin.site.register(Review)
admin.site.register(UserProfile)
