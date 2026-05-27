from django.contrib import admin

from .models import AttendanceRecord


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "school_class",
        "attendance_date",
        "status",
        "marked_by",
    )

    list_filter = (
        "status",
        "school_class",
        "attendance_date",
    )

    search_fields = (
        "student__username",
    )

    date_hierarchy = "attendance_date"