from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
)

from apps.classes.models import (
    SchoolClass,
    Enrollment,
)
from apps.classes.models import (
    SchoolClass,
)
from .models import User


class StudentSignupForm(
    UserCreationForm
):

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
    full_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:

        model = User

        fields = [
            "username",
            "full_name",
            "email",
            "password1",
            "password2",
            "school_class",
        ]

    def save(self, commit=True):

        user = super().save(
            commit=False
        )

        user.role = (
            User.Role.STUDENT
        )

        if commit:

            user.save()

            Enrollment.objects.create(
                student=user,
                school_class=self.cleaned_data[
                    "school_class"
                ],
            )

        return user
    
class StudentImportForm(forms.Form):

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

    excel_file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    default_password = forms.CharField(
        initial="123456",
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
