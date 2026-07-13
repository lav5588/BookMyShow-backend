from rest_framework.serializers import ModelSerializer

from apps.movie.models import Movie

from .models import Cinema, Location, Slot


class CinemaSerializer(ModelSerializer):
    """
    Serializer for cinema
    """

    class Meta:
        model = Cinema
        fields = ["id", "name", "location", "rows", "seats_per_row"]
        depth = 1


class CinemaMovieSerializer(ModelSerializer):
    """
    serializer for cinema based on movie
    """

    class Meta:
        model = Cinema
        fields = ["id", "name", "location", "rows", "seats_per_row", "slots"]
        depth = 1


class SlotSerializer(ModelSerializer):
    """
    Serializer for slot
    """

    class Meta:
        model = Slot
        fields = ["id", "cinema", "movie", "date_time", "price", "end_time", "language"]


class SlotsByCinemaSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            "id",
            "name",
            "languages",
            "genres",
            "description",
            "duration",
            "slug",
            "release_date",
            "slots",
            "movie_poster",
        ]
        depth = 1


class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
