import re

from unidecode import unidecode


def normalize_vietnamese_text(value):

    if not value:
        return ""

    value = str(value)

    value = value.replace(
        "\xa0",
        " ",
    )

    value = value.strip()

    value = unidecode(value)

    value = value.lower()

    value = re.sub(
        r"\s+",
        " ",
        value,
    )

    return value.strip()