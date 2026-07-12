from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone

from apps.cinema.models import Slot
from apps.user.models import User


class BookingStatus(models.TextChoices):
    BOOKED = "BOOKED"
    CANCELLED = "CANCELLED"
    PENDING = "PENDING"


class SeatBooking(models.Model):
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    row_number = models.IntegerField(validators=[MinValueValidator(1)])
    seat_number = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(
        choices=BookingStatus.choices, default=BookingStatus.PENDING
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=("row_number", "seat_number", "slot"),
                name="is_already_booked_or_pending",
                condition=Q(status=BookingStatus.BOOKED)
                | Q(status=BookingStatus.PENDING),
            )
        ]

    def __str__(self):
        return f"Ticket for {self.user.email} - Slot ID: {self.slot_id} - Seat: R{self.row_number}S{self.seat_number}"
