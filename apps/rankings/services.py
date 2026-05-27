from decimal import Decimal

from django.db.models import Avg

from apps.classes.models import (
    Enrollment,
)

from .models import (
    Exam,
    MonthlyRanking,
    RankingMonth,
    StudentScore,
)


class RankingService:

    @staticmethod
    def get_or_create_ranking_month(
        *,
        month,
        year,
    ):

        ranking_month, created = (
            RankingMonth.objects.get_or_create(
                month=month,
                year=year,
            )
        )

        return ranking_month

    @staticmethod
    def parse_scores(raw_text):

        parsed_data = []

        lines = raw_text.strip().splitlines()

        for line in lines:

            line = line.strip()

            if not line:
                continue

            parts = line.rsplit(" ", 1)

            if len(parts) != 2:
                continue

            student_name = parts[0].strip()

            try:

                score = Decimal(parts[1])

            except:

                continue

            parsed_data.append({
                "student_name": student_name,
                "score": score,
            })

        return parsed_data

    @staticmethod
    def generate_rankings(
        *,
        school_class,
        ranking_month,
    ):

        enrollments = (
            Enrollment.objects.filter(
                school_class=school_class,
                is_active=True,
            )
            .select_related("student")
        )

        ranking_data = []

        for enrollment in enrollments:

            student = enrollment.student

            average_score = (
                StudentScore.objects.filter(
                    student=student,
                    exam__school_class=school_class,
                    exam__ranking_month=ranking_month,
                )
                .aggregate(
                    average=Avg("score")
                )["average"]
            )

            average_score = (
                average_score or 0
            )

            ranking_data.append({
                "student": student,
                "average_score": average_score,
            })

        ranking_data.sort(
            key=lambda x: x["average_score"],
            reverse=True,
        )

        for index, row in enumerate(
            ranking_data,
            start=1,
        ):

            MonthlyRanking.objects.update_or_create(
                student=row["student"],
                school_class=school_class,
                ranking_month=ranking_month,
                defaults={
                    "average_score": row[
                        "average_score"
                    ],
                    "rank_position": index,
                },
            )