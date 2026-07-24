from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "priority",
        "department",
        "created_at",
    )

    list_filter = (
        "category",
        "priority",
    )

    search_fields = (
        "title",
        "description",
        "location",
        "department",
    )