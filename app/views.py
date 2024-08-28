from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, Author, Review, UserProfile, Genre
from .forms import RegistrationForm, LoginForm, UserProfileForm
from .services import create_user_profile, create_user


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")


def list_books(request: HttpRequest) -> HttpResponse:
    books: list[Book] = list(Book.objects.all())
    ctx = {"books": books}
    return render(request, "list_books.html", ctx)


def list_authors(request: HttpRequest) -> HttpResponse:
    authors: list[Author] = list(Author.objects.all())
    ctx = {"authors": authors}
    return render(request, "list_authors.html", ctx)


def edit_book(request: HttpRequest, book_id: int) -> HttpResponse:
    book: Book = Book.objects.get(id=book_id)
    if request.method == "POST":
        book.title = request.POST["title"]
        book.year = request.POST["year"]
        book.author = request.POST["author"]
        book.save()
        return redirect("index")
    return render(request, "edit_book.html", {"book": book})


def delete_book(request: HttpRequest, book_id: int) -> HttpResponse:
    book: Book = Book.objects.get(id=book_id)
    book.delete()
    return redirect("index")


def search(request: HttpRequest) -> HttpResponse:
    search_text: str = str(request.GET["query"])
    authors: list[Author] = list(Author.objects.filter(full_name__contains=search_text))
    books = Book.objects.filter(
        Q(title__contains=search_text) | Q(author__full_name__contains=search_text)
    )

    ctx = {"books": books, "authors": authors, "search_text": search_text}
    if len(books) == 0 and len(authors) == 0:
        ctx["error"] = True  # type: ignore
    return render(request, "search_books.html", context=ctx)


def get_author_info(request: HttpRequest, author_id: int) -> HttpResponse:
    author: Author = Author.objects.get(id=author_id)
    books_by_author: list[Book] = list(Book.objects.filter(author=author_id))
    ctx = {"author": author, "books": books_by_author}
    return render(request, "author_info.html", context=ctx)


# TODO: use session to store the next url. Read it at GET, pop it on POST
def login_user(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            login(request, form.cleaned_data["user"])
            return redirect("index")

        return render(request, "login.html", {"form": form})

    print(request.session.values())
    form = LoginForm()
    return render(request, "login.html", {"form": form})


def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("index")


def register_user(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            username: str = str(form.cleaned_data["username"])
            email: str = str(form.cleaned_data["email"])
            password: str = str(form.cleaned_data["password"])
            profile_picture = form.cleaned_data["profile_picture"]
            new_user = create_user(username, email, password)
            create_user_profile(new_user, profile_picture)

            return redirect("login")

        print(form.errors)
        return render(request, "register.html", {"form": form})

    form = RegistrationForm()
    return render(request, "register.html", {"form": form})


def get_user_profile(request: HttpRequest, user_id: int) -> HttpResponse:
    user_profile: UserProfile = UserProfile.objects.get(user__id=user_id)
    reviews = Review.objects.filter(added_by__id=user_id)
    books = Review.objects.filter(added_by__id=user_id).values("book").distinct()
    books_reviewed_by_user = [Book.objects.get(id=book["book"]) for book in books][:3]

    is_logged_user = user_id == request.user.id

    ctx = {
        "user_profile": user_profile,
        "reviews": reviews,
        "books_reviewed_by_user": books_reviewed_by_user,
        "is_logged_user": is_logged_user,
    }
    return render(request, "user_profile.html", ctx)


@login_required
def edit_user_profile(request: HttpRequest) -> HttpResponse:
    user_profile: UserProfile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save()

            return redirect("edit_user_profile")

        return render(request, "edit_user_profile.html", {"form": form})

    form = UserProfileForm(instance=user_profile)
    return render(request, "edit_user_profile.html", {"form": form})


def add_review_to_book(request: HttpRequest, book_id: int) -> HttpResponse:
    review_text = request.POST["review"]
    book = Book.objects.get(id=book_id)
    Review.objects.create(book=book, comment=review_text, added_by=request.user).save()

    return redirect("list_books")


def get_book_details(request: HttpRequest, book_id: int) -> HttpResponse:
    REVIEWS_NUM = 2  # TODO: change to 5 after testing
    book: Book = Book.objects.get(id=book_id)
    reviews_limit_qs: str | None = request.GET.get("reviews_limit")  # type: ignore
    reviews_limit: int = REVIEWS_NUM if not reviews_limit_qs else int(reviews_limit_qs)
    all_reviews: list[Review] = list(
        Review.objects.filter(book=book_id).order_by("-added_at")
    )
    reviews = all_reviews[:reviews_limit]
    book_genres = book.genres.all()
    similar_books = (
        Book.objects.filter(genres__in=book_genres).distinct().exclude(id=book_id)
    )

    ctx = {
        "book": book,
        "reviews_limit": reviews_limit + REVIEWS_NUM,  # For the input-field's value
        "reviews": reviews,
        "queried_all_reviews": len(reviews) >= len(all_reviews),
        "no_reviews_present": len(all_reviews) == 0,
        "similar_books": similar_books,
    }

    return render(request, "book_details.html", context=ctx)


def get_books_by_genre(request: HttpRequest, genre_slug: str) -> HttpResponse:
    genre: Genre = Genre.objects.get(slug=genre_slug)
    books = genre.book_set.all()
    ctx = {"genre": genre, "books": books}
    return render(request, "books_by_genre.html", context=ctx)
