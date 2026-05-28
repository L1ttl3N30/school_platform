from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from apps.classes.models import (
    SchoolClass,
)
from .services import (
    PaymentService,
)
from django.utils import timezone

from apps.core.decorators import (
    role_required,
)

from .forms import PaymentImportForm
from .import_service import (
    BankImportService,
)
from .models import (
    PaymentStatus,
    TuitionPayment,
)
#from .forms import (BankStatementUploadForm,)

from .reconciliation_service import (
    BankReconciliationService,
)
from django.db.models import Sum

from .models import (
    PaymentStatus,
    TuitionPayment,
)

@login_required
@role_required([
    "ADMIN",
    "TEACHER",
])
def upload_payment_file(request):

    if request.method == "POST":

        form = PaymentImportForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            batch = form.save(
                commit=False
            )

            batch.uploaded_by = (
                request.user
            )

            batch.save()

            BankImportService.process_batch(
                batch
            )

            messages.success(
                request,
                "Payment file processed successfully.",
            )

            return redirect(
                "upload_payment_file"
            )

    else:

        form = PaymentImportForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "payments/upload_payment.html",
        context,
    )


@login_required
@role_required([
    "ADMIN",
    "TEACHER",
])
def toggle_payment_status(
    request,
    payment_id,
):

    payment = get_object_or_404(
        TuitionPayment,
        id=payment_id,
    )

    if payment.status == PaymentStatus.PAID:

        payment.status = (
            PaymentStatus.PENDING
        )

        payment.paid_at = None

    else:

        payment.status = (
            PaymentStatus.PAID
        )

        payment.paid_at = timezone.now()

    payment.updated_by = request.user

    payment.save()

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "/",
        )
    )


# @login_required
# @role_required([
#     "ADMIN",
#     "TEACHER",
# ])
# def upload_bank_statement(
#     request,
# ):

#     if request.method == "POST":

#         form = (
#             BankStatementUploadForm(
#                 request.POST,
#                 request.FILES,
#             )
#         )

#         if form.is_valid():

#             result = (
#                 BankReconciliationService.process_file(
#                     uploaded_file=request.FILES[
#                         "file"
#                     ]
#                 )
#             )

#             messages.success(
#                 request,
#                 (
#                     f"Matched "
#                     f"{result['matched_count']} "
#                     f"payments."
#                 ),
#             )

#             if result["failed_rows"]:

#                 messages.warning(
#                     request,
#                     (
#                         f"{len(result['failed_rows'])} "
#                         f"transactions could not "
#                         f"be matched."
#                     ),
#                 )

#             return redirect(
#                 "upload_bank_statement"
#             )

#     else:

#         form = (
#             BankStatementUploadForm()
#         )

#     context = {
#         "form": form,
#     }

#     return render(
#         request,
#         "payments/upload_statement.html",
#         context,
#     )

@login_required
@role_required([
    "ADMIN",
    "TEACHER",
])
def payment_dashboard(
    request,
):

    payments = (
        TuitionPayment.objects.select_related(
            "student",
            "school_class",
        )
    )

    total_payments = (
        payments.count()
    )

    paid_payments = (
        payments.filter(
            status=PaymentStatus.PAID
        )
    )

    unpaid_payments = (
        payments.exclude(
            status=PaymentStatus.PAID
        )
    )

    total_collected = (
        paid_payments.aggregate(
            total=Sum("amount")
        )["total"]
        or 0
    )

    outstanding_amount = (
        unpaid_payments.aggregate(
            total=Sum("amount")
        )["total"]
        or 0
    )

    context = {
        "total_payments": total_payments,
        "paid_count": (
            paid_payments.count()
        ),
        "unpaid_count": (
            unpaid_payments.count()
        ),
        "total_collected": (
            total_collected
        ),
        "outstanding_amount": (
            outstanding_amount
        ),
        "recent_payments": (
            paid_payments.order_by(
                "-paid_at"
            )[:10]
        ),
        "unpaid_payments": (
            unpaid_payments.order_by(
                "student__full_name"
            )[:20]
        ),
    }

    return render(
        request,
        "payments/dashboard.html",
        context,
    )

@login_required
@role_required([
    "ADMIN",
    "TEACHER",
])
def generate_class_payments(
    request,
    class_id,
):

    school_class = get_object_or_404(
        SchoolClass,
        id=class_id,
    )

    month = int(
        request.GET.get("month")
    )

    year = int(
        request.GET.get("year")
    )

    updated_count = (
        PaymentService.regenerate_class_payments(
            school_class=school_class,
            month=month,
            year=year,
        )
    )

    messages.success(
        request,
        (
            f"Updated "
            f"{updated_count} "
            f"payments successfully."
        ),
    )

    return redirect(
        "monthly_attendance_grid",
        class_id=school_class.id,
    )