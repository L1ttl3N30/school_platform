from django.contrib import admin

from .models import (
    Exam,
    MonthlyRanking,
    RankingMonth,
    StudentScore,
)


admin.site.register(RankingMonth)
admin.site.register(Exam)
admin.site.register(StudentScore)
admin.site.register(MonthlyRanking)