from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class AcademicYear(TimeStampedModel):

    name = models.CharField(
        max_length=50,
        unique=True,
    )

    start_date = models.DateField()

    end_date = models.DateField()

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):

        return self.name


class SchoolClass(TimeStampedModel):

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        related_name="classes",
    )

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={
            "role": "TEACHER"
        },
        related_name="teaching_classes",
    )

    lesson_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=settings.DEFAULT_LESSON_FEE,
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):

        return self.name


class Enrollment(TimeStampedModel):

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={
            "role": "STUDENT"
        },
        related_name="enrollments",
    )

    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )

    joined_at = models.DateField(
        auto_now_add=True
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        unique_together = (
            "student",
            "school_class",
        )

    def clean(self):

        if self.student.role != "STUDENT":

            from django.core.exceptions import (
                ValidationError
            )

            raise ValidationError(
                "Only students can enroll."
            )

    def __str__(self):

        return (
            f"{self.student.username} "
            f"-> "
            f"{self.school_class.name}"
        )