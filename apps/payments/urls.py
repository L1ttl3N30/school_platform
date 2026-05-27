from django.urls import path

from .views import (
    upload_payment_file,
    toggle_payment_status,
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
]