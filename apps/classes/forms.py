from django import forms

from .models import SchoolClass


class MoveStudentForm(forms.Form):

    target_class = forms.ModelChoiceField(
        queryset=SchoolClass.objects.filter(
            is_active=True
        ),
        label="Move To Class",
    )