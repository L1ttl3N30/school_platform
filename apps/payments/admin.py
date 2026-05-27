from django.contrib import admin

from .models import TuitionPayment

from .models import (
    TuitionPayment,
    PaymentImportBatch,
    ImportedTransaction,
)
@admin.register(TuitionPayment)
class TuitionPaymentAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "school_class",
        "month",
        "year",
        "amount",
        "status",
    )

    list_filter = (
        "status",
        "month",
        "year",
        "school_class",
    )

    search_fields = (
        "student__username",
        "payment_reference",
    )

@admin.register(PaymentImportBatch)
class PaymentImportBatchAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "uploaded_by",
        "processed",
        "successful_matches",
        "failed_matches",
        "created_at",
    )


@admin.register(ImportedTransaction)
class ImportedTransactionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "amount",
        "is_matched",
        "extracted_reference",
    )

    list_filter = (
        "is_matched",
    )

    search_fields = (
        "description",
        "extracted_reference",
    )