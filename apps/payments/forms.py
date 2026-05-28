from django import forms

from .models import PaymentImportBatch


class PaymentImportForm(forms.ModelForm):

    class Meta:

        model = PaymentImportBatch

        fields = [
            "uploaded_file"
        ]

        widgets = {
            "uploaded_file": forms.FileInput(
                attrs={
                    "class": "form-control"
                }
            )
        }


# class BankStatementUploadForm(
#     forms.Form,
# ):

#     file = forms.FileField()