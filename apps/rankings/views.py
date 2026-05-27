from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    redirect,
    render,
)

from apps.accounts.models import User

from .forms import ScorePasteForm
from .models import (
    Exam,
    MonthlyRanking,
    StudentScore,
)
from .services import RankingService


@login_required
def ranking_dashboard(request):

    if request.user.role == "STUDENT":

        rankings = (
            MonthlyRanking.objects.filter(
                student=request.user
            )
            .select_related(
                "school_class",
                "ranking_month",
            )
        )

        context = {
            "rankings": rankings,
            "is_student": True,
        }

        return render(
            request,
            "rankings/student_rankings.html",
            context,
        )

    if request.method == "POST":

        form = ScorePasteForm(
            request.POST
        )

        if form.is_valid():

            school_class = (
                form.cleaned_data[
                    "school_class"
                ]
            )

            exam_name = (
                form.cleaned_data[
                    "exam_name"
                ]
            )

            month = (
                form.cleaned_data[
                    "month"
                ]
            )

            year = (
                form.cleaned_data[
                    "year"
                ]
            )

            raw_scores = (
                form.cleaned_data[
                    "raw_scores"
                ]
            )

            ranking_month = (
                RankingService
                .get_or_create_ranking_month(
                    month=month,
                    year=year,
                )
            )

            exam = Exam.objects.create(
                name=exam_name,
                school_class=school_class,
                ranking_month=ranking_month,
            )

            parsed_scores = (
                RankingService.parse_scores(
                    raw_scores
                )
            )

            created_scores = 0

            for item in parsed_scores:

                student = (
                    User.objects.filter(
                        first_name__iexact=item[
                            "student_name"
                        ]
                    ).first()
                )

                if not student:
                    continue

                StudentScore.objects.update_or_create(
                    student=student,
                    exam=exam,
                    defaults={
                        "score": item[
                            "score"
                        ]
                    },
                )

                created_scores += 1

            RankingService.generate_rankings(
                school_class=school_class,
                ranking_month=ranking_month,
            )

            messages.success(
                request,
                f"{created_scores} scores imported successfully.",
            )

            return redirect(
                "ranking_dashboard"
            )

    else:

        form = ScorePasteForm()

    leaderboard = (
        MonthlyRanking.objects.select_related(
            "student",
            "school_class",
            "ranking_month",
        )
        .order_by(
            "school_class",
            "rank_position",
        )
    )

    context = {
        "form": form,
        "leaderboard": leaderboard,
        "is_student": False,
    }

    return render(
        request,
        "rankings/teacher_rankings.html",
        context,
    )