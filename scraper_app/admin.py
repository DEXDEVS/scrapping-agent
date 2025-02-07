from django.contrib import admin
from .models import ScrapedData

@admin.register(ScrapedData)
class ScrapedDataAdmin(admin.ModelAdmin):
    list_display = ("id", "source_name", "content", "question", "answer")  # Added 'content'
    list_filter = ("content",)  # Optional: Filter by source
    search_fields = ("source_name", "question", "answer")  # Optional: Search feature
