import re

import pandas as pd

from django.db import transaction
from django.utils import timezone

from .models import (
    PaymentStatus,
    TuitionPayment,
)


class BankReconciliationService:

    REFERENCE_PATTERN = (
        r"ST\d{4}\d{4}-\d{6}"
    )

    @classmethod
    def extract_reference(
        cls,
        description,
    ):

        if not description:
            return None

        matches = re.findall(
            cls.REFERENCE_PATTERN,
            description.upper(),
        )

        if not matches:
            return None

        return matches[0]

    @classmethod
    @transaction.atomic
    def process_file(
        cls,
        *,
        uploaded_file,
    ):

        if uploaded_file.name.endswith(
            ".csv"
        ):

            dataframe = pd.read_csv(
                uploaded_file
            )

        else:

            dataframe = pd.read_excel(
                uploaded_file
            )

        matched_count = 0

        skipped_count = 0

        failed_rows = []

        for index, row in dataframe.iterrows():

            description = str(
                row.get(
                    "Description",
                    ""
                )
            ).strip()

            amount = row.get(
                "Amount",
                0,
            )

            reference = (
                cls.extract_reference(
                    description
                )
            )

            if not reference:

                failed_rows.append({
                    "row": index + 1,
                    "reason": (
                        "No payment reference found"
                    ),
                    "description": description,
                    "amount": amount,
                })

                continue

            payment = (
                TuitionPayment.objects.filter(
                    payment_reference=reference,
                ).first()
            )

            if not payment:

                failed_rows.append({
                    "row": index + 1,
                    "reason": (
                        "Payment not found"
                    ),
                    "reference": reference,
                    "description": description,
                    "amount": amount,
                })

                continue

            if (
                payment.status
                == PaymentStatus.PAID
            ):

                skipped_count += 1

                continue

            expected_amount = float(
                payment.amount
            )

            actual_amount = float(
                amount
            )

            if actual_amount < expected_amount:

                failed_rows.append({
                    "row": index + 1,
                    "reason": (
                        "Insufficient payment"
                    ),
                    "reference": reference,
                    "expected": expected_amount,
                    "actual": actual_amount,
                })

                continue

            payment.status = (
                PaymentStatus.PAID
            )

            payment.paid_at = (
                timezone.now()
            )

            payment.save(
                update_fields=[
                    "status",
                    "paid_at",
                    "updated_at",
                ]
            )

            matched_count += 1

        return {
            "matched_count": matched_count,
            "skipped_count": skipped_count,
            "failed_rows": failed_rows,
        }