from django.contrib import admin

from .forms import SlotAdminForm
from .models import Cinema, Location, Slot


@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "location",
        "rows",
        "seats_per_row",
    )
    search_fields = ("name",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("id", "location")
    search_fields = ("location",)


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "movie",
        "date_time",
        "cinema",
    )
    form = SlotAdminForm

    class Media:
        js = ("slot_admin.js",)
