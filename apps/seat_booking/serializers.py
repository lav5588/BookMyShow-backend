from django.utils import timezone
from rest_framework import serializers

from .models import BookingStatus, SeatBooking


class CancelBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatBooking
        fields = ["id"]

    def validate(self, attrs):
        request = self.context["request"]
        booking = self.instance

        if booking.user != request.user:
            raise serializers.ValidationError("You can cancel only your own bookings.")

        if booking.status != BookingStatus.BOOKED:
            raise serializers.ValidationError("Only BOOKED tickets can be cancel.")

        if booking.slot.date_time < timezone.now():
            raise serializers.ValidationError("Only future tickets can be cancel")

        return attrs

    def save(self, **kwargs):
        booking = self.instance
        booking.status = BookingStatus.CANCELLED
        booking.save(update_fields=["status"])
        return booking


class BookedSeatSerializerForSlotDetails(serializers.ModelSerializer):
    class Meta:
        model = SeatBooking
        fields = [
            "slot",
            "row_number",
            "seat_number",
            "status",
            "id",
        ]
        read_only_fields = ["id"]


class TicketSerializer(serializers.ModelSerializer):
    language = serializers.CharField(source="slot.language.language", read_only=True)
    movie = serializers.CharField(source="slot.movie.name", read_only=True)
    cinema_name = serializers.CharField(source="slot.cinema.name", read_only=True)
    cinema_location = serializers.CharField(
        source="slot.cinema.location.location", read_only=True
    )
    show_time = serializers.DateTimeField(source="slot.date_time", read_only=True)

    class Meta:
        model = SeatBooking
        fields = [
            "slot",
            "row_number",
            "seat_number",
            "user",
            "status",
            "id",
            "created_at",
            "language",
            "movie",
            "cinema_name",
            "cinema_location",
            "show_time",
        ]
