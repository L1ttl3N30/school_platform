from django.conf import settings
from django.db import models

from apps.classes.models import SchoolClass
from apps.core.models import TimeStampedModel


class AttendanceStatus(models.TextChoices):

    PRESENT = "PRESENT", "Present"
    ABSENT = "ABSENT", "Absent"
    LATE = "LATE", "Late"


class AttendanceRecord(TimeStampedModel):

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="attendance_records",
        limit_choices_to={
            "role": "STUDENT"
        },
    )

    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name="attendance_records",
    )

    attendance_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=AttendanceStatus.choices,
        default=AttendanceStatus.PRESENT,
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="marked_attendance_records",
    )

    class Meta:

        ordering = ["-attendance_date"]

        unique_together = (
            "student",
            "school_class",
            "attendance_date",
        )

        indexes = [
            models.Index(
                fields=[
                    "attendance_date"
                ]
            ),
            models.Index(
                fields=[
                    "school_class"
                ]
            ),
        ]

    def __str__(self):

        return (
            f"{self.student.username} - "
            f"{self.attendance_date} - "
            f"{self.status}"
        )