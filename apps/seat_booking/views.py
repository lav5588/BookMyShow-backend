from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.cinema.serializers import CinemaSerializer, SlotSerializer
from apps.movie.serializers import MovieSerializer

from .models import BookingStatus, SeatBooking, Slot
from .serializers import (
    BookedSeatSerializerForSlotDetails,
    CancelBookingSerializer,
    TicketSerializer,
)


class BookMultipleSeatsView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        slot_id = request.data.get("slot_id")
        seat_data = request.data.get("seats", [])

        if not seat_data:
            return Response(
                {"message": "No seats provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            slot = Slot.objects.select_related("cinema").get(id=slot_id)
        except Slot.DoesNotExist:
            return Response(
                {"message": "Invalid slot."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if slot.date_time < timezone.now():
            return Response(
                {"message": "Cannot book seats for past slots."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cinema = slot.cinema
        seen = set()
        seats = []
        query = Q()

        for seat in seat_data:
            row_number = seat.get("row_number")
            seat_number = seat.get("seat_number")

            if row_number is None or seat_number is None:
                return Response(
                    {"message": "row_number and seat_number are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if row_number < 1 or row_number > cinema.rows:
                return Response(
                    {"message": f"Invalid row_number {row_number}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if seat_number < 1 or seat_number > cinema.seats_per_row:
                return Response(
                    {"message": f"Invalid seat_number {seat_number}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            key = (row_number, seat_number)
            if key in seen:
                return Response(
                    {"message": "Duplicate seats found in request"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            query |= Q(row_number=row_number, seat_number=seat_number)
            seen.add(key)
            seats.append(key)

        existing = SeatBooking.objects.filter(
            query,
            slot=slot,
            status__in=[BookingStatus.BOOKED, BookingStatus.PENDING],
        ).exists()

        if existing:
            return Response(
                {
                    "message": "Some seats are already booked",
                    "seats": list(existing),
                },
                status=status.HTTP_409_CONFLICT,
            )

        with transaction.atomic():
            bookings = [
                SeatBooking(
                    slot=slot,
                    row_number=row,
                    seat_number=number,
                    user=request.user,
                    status=BookingStatus.BOOKED,
                )
                for row, number in seats
            ]

            SeatBooking.objects.bulk_create(bookings)

        return Response(
            {
                "message": f"{len(bookings)} seat(s) booked successfully",
            },
            status=status.HTTP_201_CREATED,
        )


class CancelBookingView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = SeatBooking.objects.all().select_related("slot", "user")
    serializer_class = CancelBookingSerializer
    http_method_names = ["patch"]

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        id = response.data["id"]
        return Response(
            {"id": id, "message": "seat cancelled successfully"},
            status=response.status_code,
        )


class UserTicketsListView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer

    def get_queryset(self):
        return (
            SeatBooking.objects.filter(
                user=self.request.user, slot__date_time__gt=timezone.now()
            )
            .select_related("slot__cinema__location", "slot__movie", "slot__language")
            .prefetch_related("slot__movie__languages")
            .order_by("-created_at")
        )


class UserPastTicketsListView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer

    def get_queryset(self):
        return (
            SeatBooking.objects.filter(
                user=self.request.user, slot__date_time__lt=timezone.now()
            )
            .select_related("slot__cinema__location", "slot__movie", "slot__language")
            .prefetch_related("slot__movie__languages")
            .order_by("-created_at")
        )


class SlotDetails(ListAPIView):
    serializer_class = BookedSeatSerializerForSlotDetails

    def get_queryset(self):
        """Optimized queryset with prefetching"""
        slot_id = self.kwargs.get("slot_id")
        slot = (
            Slot.objects.select_related("cinema", "movie", "cinema__location")
            .prefetch_related("movie__languages", "movie__genres")
            .get(id=slot_id)
        )
        if slot.date_time < timezone.now():
            raise serializers.ValidationError("this slot has been expired")
        self.movie = MovieSerializer(slot.movie).data
        self.cinema = CinemaSerializer(slot.cinema).data
        self.slot = SlotSerializer(slot).data
        return SeatBooking.objects.filter(
            Q(status=BookingStatus.BOOKED) | Q(status=BookingStatus.PENDING),
            slot_id=slot_id,
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "slot": self.slot,
                "cinema": self.cinema,
                "movie": self.movie,
                "booked_seats": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
