from django.urls import path

from .views import (
    student_signup,
    import_students,
)

urlpatterns = [

    path(
        "signup/",
        student_signup,
        name="student_signup",
    ),
    path(
    "import-students/",
    import_students,
    name="import_students",
    ),
]