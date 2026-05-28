from urllib.parse import quote

from django.conf import settings


class QRCodeService:

    BASE_URL = (
        "https://img.vietqr.io/image"
    )

    @classmethod
    def generate_vietqr_url(
        cls,
        *,
        payment,
    ):

        bank_bin = (
            settings.BANK_BIN
        )

        account_number = (
            settings.BANK_ACCOUNT_NUMBER
        )

        amount = int(
            payment.amount
        )

        description = quote(
            payment.payment_reference
        )

        account_name = quote(
            settings.BANK_ACCOUNT_NAME
        )

        return (
            f"{cls.BASE_URL}/"
            f"{bank_bin}-"
            f"{account_number}"
            f"-compact2.png"
            f"?amount={amount}"
            f"&addInfo={description}"
            f"&accountName={account_name}"
        )