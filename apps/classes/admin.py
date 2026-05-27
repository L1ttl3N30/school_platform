from django.contrib import admin

from .models import (
    AcademicYear,
    SchoolClass,
    Enrollment,
)


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "start_date",
        "end_date",
        "is_active",
    )

    list_filter = (
        "is_active",
    )


@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "teacher",
        "academic_year",
        "is_active",
    )

    list_filter = (
        "is_active",
        "academic_year",
    )

    search_fields = (
        "name",
    )
    autocomplete_fields = (
    "teacher",
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "school_class",
        "joined_at",
        "is_active",
    )

    list_filter = (
        "is_active",
        "school_class",
    )

    search_fields = (
        "student__username",
    )
    autocomplete_fields = (
    "student",
    "school_class",
    )