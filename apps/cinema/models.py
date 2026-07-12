from datetime import timedelta

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from apps.movie.models import Language, Movie


class Location(models.Model):
    """
    model representing Location
    """

    location = models.CharField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        self.location = self.location.lower().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.location


# Cinema Model
class Cinema(models.Model):
    """
    Represents a cinema venue with a specific seating layout.
    """

    name = models.CharField(max_length=100)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="cinema"
    )
    rows = models.IntegerField(validators=[MinValueValidator(1)])
    seats_per_row = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        """
        Returns a human-readable representation of the cinema, including
        cinema name and location.
        """
        return f"{self.name} at {self.location}"

    class Meta:
        """
        Ensures that no two cinema entries share the same
        combination of name and location.
        """

        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(
                fields=("name", "location"),
                name="is_name_and_location_unique",
            )
        ]


# Slot Model
class Slot(models.Model):
    """
    Represents a scheduled movie showtime within a specific cinema.
    """

    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name="slots")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="slots")
    date_time = models.DateTimeField()
    price = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(0)]
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        related_name="slots",
    )

    def __str__(self):
        """
        Returns a human-readable representation of the slot, including
        movie name, cinema name, and scheduled date/time.
        """
        return f"{self.movie.name} at {self.cinema.name} on {self.date_time}"

    class Meta:
        """
        unique_together: Ensures that the same movie cannot have duplicate
        showTimes in the same cinema at the same date and time.
        ordering: Sorts query results by date_time in ascending order.
        """

        constraints = [
            models.UniqueConstraint(
                fields=("cinema", "date_time", "movie"),
                name="cinema_movie_date_time_unique",
            ),
        ]
        ordering = ["date_time"]

    @property
    def end_time(self):
        return self.date_time + timedelta(
            minutes=self.movie.duration.total_seconds() / 60
        )

    def clean(self):
        start = self.date_time
        end = self.end_time

        if self.language not in self.movie.languages.all():
            raise ValidationError(
                {"language": "Selected language is not available for this movie."}
            )

        if self.movie.release_date and start.date() < self.movie.release_date:
            raise ValidationError(
                {
                    "date_time": "Showtime cannot be scheduled before the movie's release date."
                }
            )

        overlapping = Slot.objects.filter(cinema=self.cinema, date_time__lt=end)
        if self.pk:
            overlapping = overlapping.exclude(pk=self.pk)
        for slot in overlapping:
            if start < slot.end_time and end > slot.date_time:
                raise ValidationError(
                    "This slot time overlaps with an existing showtime"
                )

        return super().clean()
