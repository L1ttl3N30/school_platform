import base64
from io import BytesIO

import qrcode


class QRCodeService:

    @staticmethod
    def generate_base64_qr(data):

        qr = qrcode.QRCode(
            version=1,
            box_size=4,
            border=2,
        )

        qr.add_data(data)

        qr.make(fit=True)

        image = qr.make_image(
            fill_color="black",
            back_color="white",
        )

        buffer = BytesIO()

        image.save(
            buffer,
            format="PNG",
        )

        qr_base64 = base64.b64encode(
            buffer.getvalue()
        ).decode()

        return qr_base64