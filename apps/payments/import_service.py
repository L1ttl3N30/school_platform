import pandas as pd
from django.utils import timezone
from .models import (
    ImportedTransaction,
    PaymentImportBatch,
    PaymentStatus,
    TuitionPayment,
)


class BankImportService:

    @staticmethod
    def process_batch(batch):

        file_path = (
            batch.uploaded_file.path
        )

        if file_path.endswith(".csv"):

            dataframe = pd.read_csv(
                file_path
            )

        else:

            dataframe = pd.read_excel(
                file_path
            )

        success_count = 0
        failed_count = 0

        for _, row in dataframe.iterrows():

            description = str(
                row.get(
                    "description",
                    ""
                )
            )

            amount = row.get(
                "amount",
                0
            )

            extracted_reference = (
                BankImportService
                .extract_reference(
                    description
                )
            )

            matched_payment = None

            if extracted_reference:

                matched_payment = (
                    TuitionPayment.objects.filter(
                        payment_reference=extracted_reference
                    ).first()
                )

            imported_transaction = (
                ImportedTransaction.objects.create(
                    batch=batch,
                    amount=amount,
                    description=description,
                    extracted_reference=extracted_reference,
                    matched_payment=matched_payment,
                    is_matched=bool(
                        matched_payment
                    ),
                )
            )

            if matched_payment:
                matched_payment.status = (
                    PaymentStatus.PAID
                )

                matched_payment.paid_at = (
                    timezone.now()
                )
                matched_payment.save()

                success_count += 1

            else:

                failed_count += 1

        batch.processed = True

        batch.successful_matches = (
            success_count
        )

        batch.failed_matches = (
            failed_count
        )

        batch.save()

    @staticmethod
    def extract_reference(description):

        parts = description.split()

        for part in parts:

            if "_" in part:

                return part.strip()

        return None