from django.urls import path

from .views import (
    BookMultipleSeatsView,
    CancelBookingView,
    SlotDetails,
    UserPastTicketsListView,
    UserTicketsListView,
)

urlpatterns = [
    path("", BookMultipleSeatsView.as_view(), name="book-multiple-seats"),
    path("cancel/<pk>/", CancelBookingView.as_view(), name="cancel-booking"),
    path("tickets/", UserTicketsListView.as_view(), name="user-tickets"),
    path("history/", UserPastTicketsListView.as_view(), name="user-tickets"),
    path(
        "slot-details/<slot_id>/",
        SlotDetails.as_view(),
        name="seat-availability",
    ),
]
