from datetime import timedelta

from django.utils import timezone
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination

from .filters import FilterByCinema, FilterByGenre, FilterByLanguage, FilterBySlotDate
from .models import Genre, Language, Movie
from .serializers import GenreSerializer, LanguageSerializer, MovieSerializer


class MovieList(ListAPIView):
    """
    view for showing list movies based on filters based on language, genre, cinema
    """

    queryset = (
        Movie.objects.filter(slots__isnull=False, slots__date_time__gte=timezone.now())
        .prefetch_related("languages", "genres")
        .distinct()
    )
    serializer_class = MovieSerializer

    filter_backends = [
        FilterByLanguage,
        FilterByGenre,
        FilterByCinema,
        FilterBySlotDate,
    ]
    pagination_class = PageNumberPagination


class LatestMoviesList(ListAPIView):
    """views for showing latest movies"""

    serializer_class = MovieSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = (
            Movie.objects.filter(
                slots__isnull=False,
                slots__date_time__gt=timezone.now(),
                release_date__lte=timezone.now().date(),
                release_date__gte=timezone.now().date() - timedelta(days=30),
            )
            .prefetch_related("languages", "genres")
            .distinct()
        )
        return queryset


class UpcomingMoviesList(ListAPIView):
    """views for showing upcoming movies"""

    queryset = (
        Movie.objects.filter(release_date__gt=timezone.now())
        .prefetch_related("languages", "genres")
        .distinct()
    )
    serializer_class = MovieSerializer
    pagination_class = PageNumberPagination


class RetrieveMovie(RetrieveAPIView):
    """
    view for movie retrieve by movie slug
    """

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = "slug"


class LanguageView(ListAPIView):
    """
    view for language list used in movies
    """

    queryset = Language.objects.filter(
        slots__isnull=False, slots__date_time__gt=timezone.now()
    ).distinct()
    pagination_class = None
    serializer_class = LanguageSerializer


class GenreView(ListAPIView):
    """
    view for genre list used in movies
    """

    queryset = Genre.objects.filter(
        movies__slots__isnull=False, movies__slots__date_time__gt=timezone.now()
    ).distinct()
    pagination_class = None
    serializer_class = GenreSerializer
