from django.db import models
from django.utils.text import slugify

from .validators import validate_duration_field


class Language(models.Model):
    """
    model for movie language
    """

    language = models.CharField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        self.language = self.language.lower().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.language

    class Meta:
        ordering = ["id"]


class Genre(models.Model):
    """
    model for movie genre
    """

    genre = models.CharField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        self.genre = self.genre.lower().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.genre

    class Meta:
        ordering = ["id"]


# Movie Model
class Movie(models.Model):
    """
    Represents a movie in the system.

    This model stores essential information about movies including their
    name, language, genre, description, and duration. Each movie must have
    a unique name to prevent duplicates in the database.
    """

    name = models.CharField(max_length=200, unique=True)
    languages = models.ManyToManyField(to=Language, related_name="movies")
    genres = models.ManyToManyField(to=Genre, related_name="movies")
    description = models.TextField()
    duration = models.DurationField(validators=[validate_duration_field])
    slug = models.SlugField(unique=True, editable=False)
    release_date = models.DateField()
    movie_poster = models.ImageField(blank=True, upload_to="public/movies")

    class Meta:
        ordering = ["-release_date"]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns a string representation of the movie.
        """
        return f"{self.name} ({self.release_date})"
