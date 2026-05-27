from django import forms

from apps.classes.models import (
    SchoolClass,
)


class ScorePasteForm(forms.Form):

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

    exam_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
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

    raw_scores = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 15,
            }
        )
    )