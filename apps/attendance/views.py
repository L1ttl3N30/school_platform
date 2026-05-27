import calendar
from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from apps.classes.models import (
    Enrollment,
    SchoolClass,
)
from apps.core.mixins import (
    TeacherRequiredMixin,
)

from .models import (
    AttendanceRecord,
    AttendanceStatus,
)
from .services import AttendanceService
from calendar import monthrange
from datetime import datetime

from apps.payments.services import (
    PaymentService,
)
from apps.payments.qr_service import (
    QRCodeService,
)
from apps.core.decorators import (
    role_required,
)

from django.core.paginator import (
    Paginator,
)
from django.utils import timezone
from .models import (
    AttendanceRecord,
    AttendanceStatus,
)
from .forms import (
    AttendanceImportForm,
)
from .import_service import (
    AttendanceImportService,
)

@login_required
def attendance_dashboard(request):

    if request.user.role == "STUDENT":
        attendance_queryset = (
            AttendanceRecord.objects.filter(
                student=request.user
            )
            .select_related(
                "school_class"
            )
            .order_by(
                "-attendance_date"
            )
        )

        paginator = Paginator(
            attendance_queryset,
            20,
        )

        page_number = request.GET.get(
            "page"
        )

        attendance_records = paginator.get_page(
            page_number
        )

        context = {
            "attendance_records": attendance_records,
            "is_student": True,
        }

        return render(
            request,
            "attendance/student_dashboard.html",
            context,
        )

    classes = SchoolClass.objects.filter(
        is_active=True
    )

    context = {
        "classes": classes,
        "is_student": False,
    }

    return render(
        request,
        "attendance/teacher_dashboard.html",
        context,
    )


@login_required
@role_required([
    "ADMIN",
    "TEACHER",
])
def class_attendance_view(
    request,
    class_id,
):

    school_class = get_object_or_404(
        SchoolClass,
        id=class_id,
    )

    today = date.today()

    enrollments = (
        Enrollment.objects.filter(
            school_class=school_class,
            is_active=True,
        )
        .select_related("student")
    )

    attendance_map = {}

    for enrollment in enrollments:

        attendance = (
            AttendanceRecord.objects.filter(
                student=enrollment.student,
                school_class=school_class,
                attendance_date=today,
            )
            .first()
        )

        attendance_map[
            enrollment.student.id
        ] = attendance

    if request.method == "POST":

        for enrollment in enrollments:

            status = request.POST.get(
                f"status_{enrollment.student.id}"
            )

            if status:

                AttendanceService.mark_attendance(
                    student=enrollment.student,
                    school_class=school_class,
                    attendance_date=today,
                    status=status,
                    marked_by=request.user,
                )

        messages.success(
            request,
            "Attendance updated successfully.",
        )

        return redirect(
            "class_attendance",
            class_id=school_class.id,
        )

    context = {
        "school_class": school_class,
        "enrollments": enrollments,
        "attendance_map": attendance_map,
        "statuses": AttendanceStatus.choices,
        "today": today,
    }

    return render(
        request,
        "attendance/class_attendance.html",
        context,
    )



@login_required
@role_required([
    "ADMIN",
    "TEACHER",
])
def monthly_attendance_grid(
    request,
    class_id,
):

    school_class = get_object_or_404(
        SchoolClass,
        id=class_id,
    )

    month = int(
        request.GET.get(
            "month",
            date.today().month,
        )
    )

    year = int(
        request.GET.get(
            "year",
            date.today().year,
        )
    )

    total_days = monthrange(
        year,
        month,
    )[1]

    days = list(
        range(1, total_days + 1)
    )

    enrollments = (
        Enrollment.objects.filter(
            school_class=school_class,
            is_active=True,
        )
        .select_related("student")
    )

    student_rows = []

    for enrollment in enrollments:

        student = enrollment.student

        attendance_records = (
            AttendanceRecord.objects.filter(
                student=student,
                school_class=school_class,
                attendance_date__year=year,
                attendance_date__month=month,
            )
        )

        attendance_map = {
            record.attendance_date.day:
            record.status
            for record in attendance_records
        }

        total_present = (
            attendance_records.filter(
                status="PRESENT"
            ).count()
        )

        payment = (
            PaymentService.get_or_create_payment(
                student=student,
                school_class=school_class,
                month=month,
                year=year,
            )
        )

        qr_data = (
            payment.payment_reference
        )

        qr_code = (
            QRCodeService.generate_base64_qr(
                qr_data
            )
        )

        student_rows.append({
            "student": student,
            "attendance_map": attendance_map,
            "total_present": total_present,
            "payment": payment,
            "qr_code": qr_code,
        })

    context = {
        "school_class": school_class,
        "student_rows": student_rows,
        "days": days,
        "month": month,
        "year": year,
    }

    return render(
        request,
        "attendance/monthly_grid.html",
        context,
    )

@login_required
@role_required([
    "ADMIN",
    "TEACHER",
])
def toggle_attendance(
    request,
    class_id,
    student_id,
    year,
    month,
    day,
):

    school_class = get_object_or_404(
        SchoolClass,
        id=class_id,
    )

    attendance_date = date(
        year,
        month,
        day,
    )

    attendance = (
        AttendanceRecord.objects.filter(
            student_id=student_id,
            school_class=school_class,
            attendance_date=attendance_date,
        ).first()
    )

    if attendance:

        attendance.delete()

    else:

        AttendanceRecord.objects.create(
            student_id=student_id,
            school_class=school_class,
            attendance_date=attendance_date,
            status=AttendanceStatus.PRESENT,
            marked_by=request.user,
        )

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "/",
        )
    )

@login_required
@role_required([
    "ADMIN",
    "TEACHER",
])
def import_attendance_excel(request):

    if request.method == "POST":

        form = AttendanceImportForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            result = (
                AttendanceImportService.import_excel(
                    excel_file=request.FILES[
                        "excel_file"
                    ],
                    school_class=form.cleaned_data[
                        "school_class"
                    ],
                    month=form.cleaned_data[
                        "month"
                    ],
                    year=form.cleaned_data[
                        "year"
                    ],
                    marked_by=request.user,
                )
            )

            messages.success(
                request,
                (
                    f"Imported "
                    f"{result['imported_count']} "
                    f"attendance records. "
                    f"Skipped "
                    f"{result['skipped_count']} students."
                ),
            )

            return redirect(
                "import_attendance_excel"
            )

    else:

        form = AttendanceImportForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "attendance/import_excel.html",
        context,
    )