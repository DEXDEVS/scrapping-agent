from django.contrib import admin
from .models import ScrapedData

@admin.register(ScrapedData)
class ScrapedDataAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "source_name", "short_content", "question", "answer", "created_at")
    list_filter = ("created_at", "user", "source_name")  # Filter by date, user, and source
    search_fields = ("source_name", "content", "question", "answer")  # Search through fields
    ordering = ("-created_at",)  # Show the latest entries first
    list_per_page = 20  # Pagination: Show 20 entries per page
    readonly_fields = ("created_at", "updated_at")  # Prevent changes to timestamps

    def short_content(self, obj):
        return obj.content[:75] + "..." if len(obj.content) > 75 else obj.content  # Show preview of content

    short_content.short_description = "Content Preview"  # Rename column

