from django.forms import ValidationError
import re


def validate_alphanum_username(value: str) -> None:
    if not value.isalnum():
        raise ValidationError("Username must consists only of letters and numbers")


def validate_begin_with_letter_username(value: str) -> None:
    if not value[0].isalpha():
        raise ValidationError("Username must begin with a letter")


def validate_password(value: str) -> None:
    has_capital_letter = re.search(r"[A-Z]", value) is not None
    has_special_character = re.search(r"[\.\,\@\!\?\/\*\+\-\s^]", value) is not None
    has_digit = re.search(r"\d", value) is not None

    if not has_capital_letter:
        raise ValidationError("Password must contain at least one capital letter")

    if not has_special_character:
        raise ValidationError(
            "Password must contain at least one special character .,@!?/*+-^"
        )

    if not has_digit:
        raise ValidationError("Password must contain at least one digit")
