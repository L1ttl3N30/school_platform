from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Information",
            {
                "fields": (
                    "role",
                    "phone_number",
                    "date_of_birth",
                    "avatar",
                    "full_name",
                    "student_code",
                )
            },
        ),
    )

    list_display = (
        "username",
        "full_name",
        "student_code",
        "email",
        "role",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "role",
        "is_staff",
        "is_active",
    )
    search_fields = (
    "username",
    "full_name",
    "student_code",
    "email",
    )
    ordering = (
    "username",
    )