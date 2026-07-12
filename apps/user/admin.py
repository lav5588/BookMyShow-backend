# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ["id", "email", "name", "is_staff", "password", "is_active"]
    list_filter = ["is_staff", "is_superuser"]
    search_fields = ["email", "name"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("name", "phone_number", "profile_pic")}),
        (
            "permissions",
            {"fields": ("is_active", "is_staff", "groups", "user_permissions")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "phone_number",
                    "is_superuser",
                    "is_staff",
                )
            },
        ),
    )
    ordering = ("email",)
