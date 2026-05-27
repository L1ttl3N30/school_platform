from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
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