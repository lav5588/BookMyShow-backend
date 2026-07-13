from rest_framework.filters import BaseFilterBackend


class FilterByLanguage(BaseFilterBackend):
    """
    filter movie based on language
    """

    def filter_queryset(self, request, queryset, view):
        languages_str = request.query_params.get("languages")
        if languages_str:
            languages = languages_str.split(",")
            queryset = queryset.filter(languages__language__in=languages).distinct()
        return queryset


class FilterByGenre(BaseFilterBackend):
    """
    filter movie based on genre
    """

    def filter_queryset(self, request, queryset, view):
        genres_str = request.query_params.get("genres")

        if genres_str:
            genres = genres_str.split(",")
            queryset = queryset.filter(genresgenrein=genres).distinct()
        return queryset


class FilterByCinema(BaseFilterBackend):
    """
    filter movie based on cinema id
    """

    def filter_queryset(self, request, queryset, view):
        cinema_id = request.query_params.get("cinema")
        if cinema_id:
            queryset = queryset.filter(slotscinemaid=cinema_id).distinct()
        return queryset


class FilterBySlotDate(BaseFilterBackend):
    """
    filter movies based on the slot dates
    """

    def filter_queryset(self, request, queryset, view):
        slot_date = request.query_params.get("slot_date")
        if slot_date:
            queryset = queryset.filter(slots__date_time__date=slot_date).distinct()
        return queryset
