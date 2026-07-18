from django.contrib import admin

from .models import ContactUsQuery


@admin.register(ContactUsQuery)
class ContactUsQueryAdmin(admin.ModelAdmin):
    list_display = ("email", "created_at", "query_snippet")
    search_fields = ("email", "query")
    list_filter = ("created_at",)

    def query_snippet(self, obj):
        return obj.query[:50] + ("..." if len(obj.query) > 50 else "")

    query_snippet.short_description = "Query Snippet"
