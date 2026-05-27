from datetime import date

import openpyxl

from apps.accounts.models import User

from .models import (
    AttendanceRecord,
    AttendanceStatus,
)


class AttendanceImportService:

    @staticmethod
    def import_excel(
        *,
        excel_file,
        school_class,
        month,
        year,
        marked_by,
    ):

        workbook = openpyxl.load_workbook(
            excel_file
        )

        sheet = workbook.active

        imported_count = 0
        skipped_count = 0

        # DAY COLUMNS:
        # C = 3
        # AG = 33

        START_DAY_COLUMN = 3
        END_DAY_COLUMN = 33

        for row in range(3, sheet.max_row + 1):

            student_name = (
                sheet.cell(
                    row=row,
                    column=2,
                ).value
            )

            if not student_name:

                continue


            student_name = (
                str(student_name)
                .replace("\xa0", " ")
                .strip()
            )

            print(
                "EXCEL NAME:",
                repr(student_name)
            )

            student = (
                User.objects.filter(
                    full_name__icontains=student_name
                ).first()
            )
            print(
                "MATCHED:",
                student
            )

            if not student:

                skipped_count += 1
                continue

            for column in range(
                START_DAY_COLUMN,
                END_DAY_COLUMN + 1,
            ):

                day = (
                    column
                    - START_DAY_COLUMN
                    + 1
                )

                cell_value = (
                    sheet.cell(
                        row=row,
                        column=column,
                    ).value
                )

                if str(cell_value).strip() != "1":

                    continue

                attendance_date = date(
                    year,
                    month,
                    day,
                )

                AttendanceRecord.objects.update_or_create(
                    student=student,
                    school_class=school_class,
                    attendance_date=attendance_date,
                    defaults={
                        "status": (
                            AttendanceStatus.PRESENT
                        ),
                        "marked_by": marked_by,
                    },
                )

                imported_count += 1

        return {
            "imported_count": imported_count,
            "skipped_count": skipped_count,
        }