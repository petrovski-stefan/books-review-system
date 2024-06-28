from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, Author, Review, UserProfile


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


def search_books(request: HttpRequest) -> HttpResponse:
    search_text: str = str(request.GET["query"])
    books = Book.objects.filter(
        Q(title__contains=search_text) | Q(author__name__contains=search_text)
    )
    ctx = {"books": books, "search_text": search_text}  # type: ignore
    return render(request, "search_books.html", context=ctx)


def get_author_info(request: HttpRequest, author_id: int) -> HttpResponse:
    author: Author = Author.objects.get(id=author_id)
    books_by_author: list[Book] = list(Book.objects.filter(author=author_id))
    ctx = {"author": author, "books": books_by_author}
    return render(request, "author_info.html", context=ctx)


# TODO: use session to store the next url. Read it at GET, pop it on POST
def login_user(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        print(request.session.values())
        return render(request, "login.html")

    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect("index")
    else:
        ctx = {"username": username, "password": password, "error": True}
        return render(request, "login.html", ctx)


def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("index")


def register_user(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, "register.html")

    username: str = str(request.POST["username"])
    email: str = str(request.POST["email"])
    password: str = str(request.POST["password"])
    repeat_password: str = str(request.POST["repeat_password"])

    ctx: dict[str, str | bool] = {"username": username, "password": password}

    if password != repeat_password:
        ctx["error"] = True
        return render(request, "register.html", ctx)

    new_user = User.objects.create_user(
        username=username, email=email, password=password
    )
    new_user.save()
    UserProfile.objects.create(user=new_user)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect("index")
    else:
        ctx = {"username": username, "password": password, "error": True}
        return render(request, "login.html", ctx)


def get_user_profile(request: HttpRequest, user_id: int) -> HttpResponse:
    user_profile: UserProfile = UserProfile.objects.get(user__id=user_id)
    reviews = Review.objects.filter(added_by__id=user_id)
    books = Review.objects.filter(added_by__id=user_id).values("book").distinct()
    books_reviewed_by_user = [Book.objects.get(id=book["book"]) for book in books][:3]

    ctx = {
        "user_profile": user_profile,
        "reviews": reviews,
        "books_reviewed_by_user": books_reviewed_by_user,
    }
    return render(request, "user_profile.html", ctx)


@login_required
def edit_user_profile(request: HttpRequest, user_id: int) -> HttpResponse:
    user_profile: UserProfile = UserProfile.objects.get(user__id=user_id)

    if request.method == "GET":
        ctx = {"user_profile": user_profile}
        return render(request, "edit_user_profile.html", ctx)

    user_profile.age = request.POST["age"]
    user_profile.country = request.POST["country"]
    user_profile.save()
    ctx = {"user_profile": user_profile}
    return render(request, "user_profile.html", ctx)


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

    ctx = {
        "book": book,
        "reviews_limit": reviews_limit + REVIEWS_NUM,  # For the input-field's value
        "reviews": reviews,
        "queried_all_reviews": len(reviews) >= len(all_reviews),
        "no_reviews_present": len(all_reviews) == 0,
    }

    return render(request, "book_details.html", context=ctx)
