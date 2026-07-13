from rest_framework.filters import BaseFilterBackend


class FilterByLocation(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        location = request.query_params.get("location")
        if location:
            queryset = queryset.filter(location__location__iexact=location)
        return queryset
