from decimal import Decimal

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from apps.attendance.models import (
    AttendanceRecord,
    AttendanceStatus,
)
from apps.classes.models import (
    Enrollment,
)

from .models import (
    PaymentStatus,
    TuitionPayment,
)


class PaymentService:

    DEFAULT_LESSON_FEE = Decimal(
        str(settings.DEFAULT_LESSON_FEE)
    )

    @classmethod
    def calculate_monthly_amount(
        cls,
        *,
        student,
        school_class,
        month,
        year,
    ):

        total_present = (
            AttendanceRecord.objects.filter(
                student=student,
                school_class=school_class,
                attendance_date__month=month,
                attendance_date__year=year,
                status=AttendanceStatus.PRESENT,
            ).count()
        )

        lesson_fee = (
            school_class.lesson_fee
            or cls.DEFAULT_LESSON_FEE
        )

        return (
            Decimal(total_present)
            * Decimal(lesson_fee)
        )

    @staticmethod
    def generate_payment_reference(
        *,
        student,
        month,
        year,
    ):

        return (
            f"{student.reference_number}"
            f"-"
            f"{month:02d}"
            f"{year}"
        )

    @classmethod
    @transaction.atomic
    def get_or_create_payment(
        cls,
        *,
        student,
        school_class,
        month,
        year,
    ):

        existing_payment = (
            TuitionPayment.objects.filter(
                student=student,
                school_class=school_class,
                month=month,
                year=year,
            ).first()
        )

        if existing_payment:

            return existing_payment, False

        if not student.reference_number:

            raise ValueError(
                (
                    f"Student "
                    f"{student.full_name} "
                    f"does not have "
                    f"a reference number."
                )
            )

        reference = (
            cls.generate_payment_reference(
                student=student,
                month=month,
                year=year,
            )
        )

        payment = (
            TuitionPayment.objects.create(
                student=student,
                school_class=school_class,
                month=month,
                year=year,
                amount=cls.calculate_monthly_amount(
                    student=student,
                    school_class=school_class,
                    month=month,
                    year=year,
                ),
                payment_reference=reference,
                status=PaymentStatus.PENDING,
            )
        )

        return payment, True

    @staticmethod
    def mark_as_paid(
        payment,
        *,
        updated_by=None,
    ):

        payment.status = (
            PaymentStatus.PAID
        )

        payment.paid_at = (
            timezone.now()
        )

        payment.updated_by = (
            updated_by
        )

        payment.save(
            update_fields=[
                "status",
                "paid_at",
                "updated_by",
                "updated_at",
            ]
        )

        return payment

    @classmethod
    @transaction.atomic
    def generate_monthly_payments(
        cls,
        *,
        school_class,
        students,
        month,
        year,
    ):

        created_count = 0

        for student in students:

            if not student.reference_number:
                continue

            _, created = (
                cls.get_or_create_payment(
                    student=student,
                    school_class=school_class,
                    month=month,
                    year=year,
                )
            )

            if created:
                created_count += 1

        return created_count

    @classmethod
    def recalculate_payment_amount(
        cls,
        *,
        payment,
    ):

        new_amount = (
            cls.calculate_monthly_amount(
                student=payment.student,
                school_class=payment.school_class,
                month=payment.month,
                year=payment.year,
            )
        )

        payment.amount = new_amount

        payment.save(
            update_fields=[
                "amount",
                "updated_at",
            ]
        )

        return payment

    @classmethod
    @transaction.atomic
    def regenerate_class_payments(
        cls,
        *,
        school_class,
        month,
        year,
    ):

        payments_updated = 0

        enrollments = (
            Enrollment.objects.filter(
                school_class=school_class,
                is_active=True,
            )
            .select_related("student")
            .order_by(
                "student__full_name"
            )
        )

        for enrollment in enrollments:

            student = enrollment.student

            if not student.reference_number:
                continue

            payment, _ = (
                cls.get_or_create_payment(
                    student=student,
                    school_class=school_class,
                    month=month,
                    year=year,
                )
            )

            cls.recalculate_payment_amount(
                payment=payment
            )

            payments_updated += 1

        return payments_updated