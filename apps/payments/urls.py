from django.urls import path

from .views import (
    upload_payment_file,
    toggle_payment_status,
    generate_class_payments,
)
#from .views import (upload_bank_statement,)
from .views import (
    payment_dashboard,
)
urlpatterns = [

    path(
        "upload/",
        upload_payment_file,
        name="upload_payment_file",
        
    ),
    path(
    "toggle/<int:payment_id>/",
    toggle_payment_status,
    name="toggle_payment_status",
    ),

    path(
    "",
    payment_dashboard,
    name="payment_dashboard",
    ),path(
    "generate/<int:class_id>/",
    generate_class_payments,
    name="generate_class_payments",
   ),
]

#    path("reconcile/",upload_bank_statement,name="upload_bank_statement",),