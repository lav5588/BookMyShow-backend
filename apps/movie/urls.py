from django.urls import path

# from apps.cinema.views import MovieLanguageListAPIView, SlotsByMovieSlug
from .views import (
    GenreView,
    LanguageView,
    LatestMoviesList,
    MovieList,
    RetrieveMovie,
    UpcomingMoviesList,
)

urlpatterns = [
    path("languages/", LanguageView.as_view(), name="language-list"),
    path("genres/", GenreView.as_view(), name="genre-list"),
    path("", MovieList.as_view(), name="movie-list"),
    path("latest/", LatestMoviesList.as_view(), name="latest-movies"),
    path("upcoming/", UpcomingMoviesList.as_view(), name="upcoming-movies"),
    path("<slug:slug>/", RetrieveMovie.as_view(), name="movie-detail"),
    # path(
    #     "<slug:slug>/movie-slots/",
    #     SlotsByMovieSlug.as_view(),
    #     name="slots-by-movie-slug",
    # ),
    # path(
    #     "<int:movie_id>/languages/",
    #     MovieLanguageListAPIView.as_view(),
    #     name="movie-language-list",
    # ),
]
