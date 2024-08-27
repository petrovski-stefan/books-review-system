from django import forms
from django.contrib.auth.models import User
from .form_validators import (
    validate_begin_with_letter_username,
    validate_alphanum_username,
    validate_password,
)
from django.contrib.auth import authenticate


class RegistrationForm(forms.Form):
    username = forms.CharField(
        min_length=5,
        max_length=21,
        validators=[validate_alphanum_username, validate_begin_with_letter_username],
    )
    email = forms.EmailField(required=False)
    profile_picture = forms.ImageField(required=False)
    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8,
        max_length=21,
        validators=[validate_password],
    )
    repeat_password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8,
        max_length=21,
        # validators=[validate_password],
    )

    def clean_username(self) -> str:
        username: str = self.cleaned_data.get("username")  # type: ignore

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")

        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        repeat_password = cleaned_data.get("repeat_password")

        if password and repeat_password and password != repeat_password:
            # Accessible in the __all__ key in form.errors
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(
        min_length=5,
        max_length=21,
        validators=[validate_alphanum_username, validate_begin_with_letter_username],
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8,
        max_length=21,
        validators=[validate_password],
    )

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Wrong credentials. Try again.")

        cleaned_data["user"] = user

        return cleaned_data
