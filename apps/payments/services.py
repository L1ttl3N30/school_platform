from decimal import Decimal

from .models import (
    PaymentStatus,
    TuitionPayment,
)


class PaymentService:

    DEFAULT_MONTHLY_FEE = Decimal("500000")

    @staticmethod
    def generate_payment_reference(
        *,
        student,
        school_class,
        month,
        year,
    ):

        return (
            f"{school_class.name}_"
            f"{year}_"
            f"{month}_"
            f"{student.id}"
        )

    @staticmethod
    def get_or_create_payment(
        *,
        student,
        school_class,
        month,
        year,
    ):

        reference = (
            PaymentService.generate_payment_reference(
                student=student,
                school_class=school_class,
                month=month,
                year=year,
            )
        )

        payment, created = (
            TuitionPayment.objects.get_or_create(
                student=student,
                school_class=school_class,
                month=month,
                year=year,
                defaults={
                    "amount": (
                        PaymentService
                        .DEFAULT_MONTHLY_FEE
                    ),
                    "payment_reference": reference,
                },
            )
        )

        return payment

    @staticmethod
    def mark_as_paid(payment):

        payment.status = PaymentStatus.PAID
        payment.save()

        return payment