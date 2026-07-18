from django.urls import path

from .views import (
    AvailableUpcomingSlotsDatesByCinema,
    CinemaList,
    LocationList,
    RetrieveCinema,
    SlotsByCinema,
)

urlpatterns = [
    path("", CinemaList.as_view(), name="cinema-list"),
    path("locations/", LocationList.as_view(), name="location-list"),
    path("<int:pk>/", RetrieveCinema.as_view(), name="cinema-detail"),
    path("<int:pk>/movie-slots/", SlotsByCinema.as_view(), name="slots-by-cinema"),
    path(
        "<int:pk>/available-slots-dates/",
        AvailableUpcomingSlotsDatesByCinema.as_view(),
        name="available-slots-dates-by-cinema",
    ),
]
