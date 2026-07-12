from rest_framework.serializers import ModelSerializer

from .models import Genre, Language, Movie


class MovieSerializer(ModelSerializer):
    """
    serializer for movie
    """

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
            "movie_poster",
        ]
        extra_kwargs = {"slug": {"read_only": True}}
        depth = 1


class LanguageSerializer(ModelSerializer):
    """
    serializer for language
    """

    class Meta:
        model = Language
        fields = ["id", "language"]


class GenreSerializer(ModelSerializer):
    """
    serializer for genre
    """

    class Meta:
        model = Genre
        fields = ["id", "genre"]
