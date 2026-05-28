from django.db.models import Max

from .models import User


class StudentReferenceService:

    PREFIX = "ST"

    YEAR = "2026"

    @classmethod
    def get_next_number(cls):

        latest_reference = (
            User.objects.filter(
                reference_number__isnull=False
            ).aggregate(
                max_ref=Max(
                    "reference_number"
                )
            )["max_ref"]
        )

        if not latest_reference:

            return 1

        latest_number = int(
            latest_reference[6:]
        )

        return latest_number + 1

    @classmethod
    def generate_reference_number(
        cls,
        number,
    ):

        return (
            f"{cls.PREFIX}"
            f"{cls.YEAR}"
            f"{number:04d}"
        )
    

