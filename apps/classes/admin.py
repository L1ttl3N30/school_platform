from django.contrib import admin

from .models import (
    Enrollment,
    SchoolClass,
)


@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "name",
        "lesson_fee",
        "is_active",
    ]

    list_filter = [
        "is_active",
    ]

    search_fields = [
        "name",
    ]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):

    list_display = [
        "student",
        "school_class",
        "is_active",
        "created_at",
    ]

    list_filter = [
        "is_active",
        "school_class",
    ]

    search_fields = [
        "student__full_name",
        "student__username",
        "student__reference_number",
    ]

    autocomplete_fields = [
        "student",
        "school_class",
    ]