from django.contrib import admin

from .models import SeatBooking


# Register your models here.
@admin.register(SeatBooking)
class SeatBookingAdmin(admin.ModelAdmin):
    list_display = ("id", "slot", "user", "row_number", "seat_number", "status", "created_at")
