from datetime import timedelta

from django.core.exceptions import ValidationError


def validate_duration_field(value):
    if value > timedelta(hours=5):
        raise ValidationError("Duration of movie cannot exceed 5 hours.")
    elif value < timedelta(hours=1):
        raise ValidationError("duration of movie should be at least 1 hour.")
