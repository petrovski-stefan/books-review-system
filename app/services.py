from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile

from .models import UserProfile


def create_user(username: str, email: str, password: str) -> User:
    return User.objects.create_user(username=username, email=email, password=password)


def create_user_profile(
    user: User, profile_picture: UploadedFile | None
) -> UserProfile:
    if profile_picture:
        return UserProfile.objects.create(user=user, profile_picture=profile_picture)

    return UserProfile.objects.create(user=user)
