from django.conf import settings
from django.db import models

from apps.classes.models import SchoolClass
from apps.core.models import TimeStampedModel


class PaymentStatus(models.TextChoices):

    PENDING = "PENDING", "Pending"
    PAID = "PAID", "Paid"

class TuitionPayment(TimeStampedModel):

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tuition_payments",
        limit_choices_to={
            "role": "STUDENT"
        },
    )

    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name="tuition_payments",
    )

    month = models.IntegerField()

    year = models.IntegerField()

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    payment_reference = models.CharField(
        max_length=255,
        unique=True,
    )

    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )

    paid_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_payments",
    )

    class Meta:

        unique_together = (
            "student",
            "school_class",
            "month",
            "year",
        )

        ordering = [
            "-year",
            "-month",
        ]

        indexes = [
            models.Index(
                fields=[
                    "payment_reference"
                ]
            )
        ]

    def __str__(self):

        return (
            f"{self.student.username} "
            f"- "
            f"{self.month}/{self.year}"
        )
    


class PaymentImportBatch(TimeStampedModel):

    uploaded_file = models.FileField(
        upload_to="payment_uploads/"
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    processed = models.BooleanField(
        default=False
    )

    successful_matches = models.IntegerField(
        default=0
    )

    failed_matches = models.IntegerField(
        default=0
    )

    def __str__(self):

        return (
            f"Import Batch "
            f"{self.id}"
        )


class ImportedTransaction(TimeStampedModel):

    batch = models.ForeignKey(
        PaymentImportBatch,
        on_delete=models.CASCADE,
        related_name="transactions",
    )

    transaction_date = models.DateField(
        null=True,
        blank=True,
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    description = models.TextField()

    extracted_reference = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    matched_payment = models.ForeignKey(
        TuitionPayment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    is_matched = models.BooleanField(
        default=False
    )

    def __str__(self):

        return self.description