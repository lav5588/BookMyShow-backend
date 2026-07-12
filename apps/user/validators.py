import re

from django.core.exceptions import ValidationError


class PasswordValidator:
    def validate(self, password, user=None):
        if not re.match(
            r"(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$",
            password,
        ):
            raise ValidationError(
                "Password must contain at least 8 characters, at least one number, both lower and upper case letters, at least one special character #, ? , !"
            )

    def get_help_text(self):
        return "Password must contain at least 8 characters, at least one number, both lower and upper case letters, at least one special character #, ? , !"
