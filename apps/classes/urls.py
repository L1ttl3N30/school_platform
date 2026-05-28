from django.urls import path

from .views import (
    move_student_to_class,
    remove_student_from_class,
)

urlpatterns = [

    path(
        "enrollment/<int:enrollment_id>/move/",
        move_student_to_class,
        name="move_student_to_class",
    ),

    path(
        "enrollment/<int:enrollment_id>/remove/",
        remove_student_from_class,
        name="remove_student_from_class",
    ),
]