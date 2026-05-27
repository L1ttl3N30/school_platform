from django import forms

from .models import (
    AttendanceRecord,
    AttendanceStatus,
)


class AttendanceForm(forms.ModelForm):

    class Meta:

        model = AttendanceRecord

        fields = [
            "status",
            "notes",
        ]

        widgets = {
            "status": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                }
            ),
        }

from django import forms

from apps.classes.models import (
    SchoolClass,
)


class AttendanceImportForm(forms.Form):

    school_class = forms.ModelChoiceField(
        queryset=SchoolClass.objects.filter(
            is_active=True
        ),
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        ),
    )

    month = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    year = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    excel_file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "class": "form-control"
            }
        )
    )