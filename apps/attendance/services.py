from datetime import date

from .models import AttendanceRecord


class AttendanceService:

    @staticmethod
    def mark_attendance(
        *,
        student,
        school_class,
        attendance_date,
        status,
        marked_by,
        notes="",
    ):

        attendance, created = (
            AttendanceRecord.objects.update_or_create(
                student=student,
                school_class=school_class,
                attendance_date=attendance_date,
                defaults={
                    "status": status,
                    "marked_by": marked_by,
                    "notes": notes,
                },
            )
        )

        return attendance

    @staticmethod
    def get_monthly_attendance(
        *,
        school_class,
        year,
        month,
    ):

        return AttendanceRecord.objects.filter(
            school_class=school_class,
            attendance_date__year=year,
            attendance_date__month=month,
        ).select_related(
            "student"
        )