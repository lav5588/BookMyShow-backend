from django.db.models import Prefetch
from django.utils import timezone
from rest_framework.generics import ListAPIView, RetrieveAPIView

from apps.movie.models import Language, Movie
from apps.movie.serializers import LanguageSerializer

from .filters import FilterByLocation
from .models import Cinema, Location, Slot
from .serializers import (
    CinemaMovieSerializer,
    CinemaSerializer,
    LocationSerializer,
    SlotsByCinemaSerializer,
)


class SlotsByMovieSlug(ListAPIView):
    """
    List of cinemas filter by movie
    """

    serializer_class = CinemaMovieSerializer
    pagination_class = None

    def get_queryset(self):
        slug = self.kwargs["slug"]
        date = self.request.query_params.get("date")
        slot_query = Slot.objects.filter(
            movie__slug=slug,
            date_time__gte=timezone.now(),
            date_time__date=date,
        )
        prefetch_slots = Prefetch("slots", queryset=slot_query)

        return (
            Cinema.objects.filter(
                slots__movie__slug=slug,
                slots__date_time__gte=timezone.now(),
                slots__date_time__date=date,
            )
            .select_related("location")
            .prefetch_related(
                prefetch_slots,
            )
            .distinct()
        )


class CinemaList(ListAPIView):
    queryset = (
        Cinema.objects.filter(slots__isnull=False, slots__date_time__gte=timezone.now())
        .select_related("location")
        .distinct()
    )
    serializer_class = CinemaSerializer
    filter_backends = [FilterByLocation]
    pagination_class = None


class RetrieveCinema(RetrieveAPIView):
    queryset = Cinema.objects.select_related("location").all()
    serializer_class = CinemaSerializer


class SlotsByCinema(ListAPIView):
    serializer_class = SlotsByCinemaSerializer
    pagination_class = None

    def get_queryset(self):
        pk = self.kwargs["pk"]
        date = self.request.query_params.get("date")
        slot_query = Slot.objects.filter(
            cinema__id=pk,
            date_time__gte=timezone.now(),
            date_time__date=date,
        )
        prefetch_slots = Prefetch("slots", queryset=slot_query)

        return (
            Movie.objects.filter(
                slots__cinema_id=pk,
                slots__date_time__gte=timezone.now(),
                slots__date_time__date=date,
            )
            .prefetch_related(prefetch_slots, "languages", "genres")
            .distinct()
        )


class LocationList(ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    pagination_class = None


class MovieLanguageListAPIView(ListAPIView):
    serializer_class = LanguageSerializer

    def get_queryset(self):
        movie_id = self.kwargs["movie_id"]

        return Language.objects.filter(movies__id=movie_id).distinct()
