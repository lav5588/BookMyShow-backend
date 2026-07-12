from django.contrib import admin

from .models import Genre, Language, Movie


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "genre")
    search_fields = ("genre",)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("id", "language")
    search_fields = ("language",)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    readonly_fields = ("slug",)
    list_display = (
        "id",
        "name",
        "description",
        "duration",
        "slug",
        "release_date",
        "movie_poster",
    )
