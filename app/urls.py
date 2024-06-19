from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:book_id>/edit", views.edit_book, name="edit_book"),
    path("<int:book_id>/delete", views.delete_book, name="delete_book"),

    path("books", views.list_books, name="list_books"),

    path("authors/<int:author_id>", views.get_author_info, name="author_info"),
    path("authors", views.list_authors, name="list_authors"),

    path("search", views.search_books, name="search_books"),

    # Auth
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("register", views.register_user, name="register"),

    # Profile
    path("user/<int:user_id>", views.get_user_profile, name="user_profile"),
    path("user/<int:user_id>/edit", views.edit_user_profile, name="edit_user_profile"),
]
