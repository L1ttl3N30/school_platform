from django.conf import settings
from django.db import models

from apps.classes.models import SchoolClass
from apps.core.models import TimeStampedModel


class RankingMonth(TimeStampedModel):

    month = models.IntegerField()

    year = models.IntegerField()

    is_active = models.BooleanField(
        default=True
    )

    class Meta:

        unique_together = (
            "month",
            "year",
        )

        ordering = [
            "-year",
            "-month",
        ]

    def __str__(self):

        return f"{self.month}/{self.year}"


class Exam(TimeStampedModel):

    name = models.CharField(
        max_length=255
    )

    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name="exams",
    )

    ranking_month = models.ForeignKey(
        RankingMonth,
        on_delete=models.CASCADE,
        related_name="exams",
    )

    class Meta:

        ordering = ["name"]

    def __str__(self):

        return (
            f"{self.name} - "
            f"{self.school_class.name}"
        )


class StudentScore(TimeStampedModel):

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_scores",
        limit_choices_to={
            "role": "STUDENT"
        },
    )

    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="scores",
    )

    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    class Meta:

        unique_together = (
            "student",
            "exam",
        )

    def __str__(self):

        return (
            f"{self.student.username} "
            f"- "
            f"{self.score}"
        )


class MonthlyRanking(TimeStampedModel):

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="monthly_rankings",
        limit_choices_to={
            "role": "STUDENT"
        },
    )

    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name="monthly_rankings",
    )

    ranking_month = models.ForeignKey(
        RankingMonth,
        on_delete=models.CASCADE,
        related_name="monthly_rankings",
    )

    average_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    rank_position = models.IntegerField(
        default=0
    )

    class Meta:

        ordering = [
            "rank_position"
        ]

        unique_together = (
            "student",
            "school_class",
            "ranking_month",
        )
        indexes = [
            models.Index(
                fields=[
                    "school_class",
                    "ranking_month",
                ]
            )
        ]

    def __str__(self):

        return (
            f"{self.student.username} "
            f"- Rank "
            f"{self.rank_position}"
        )