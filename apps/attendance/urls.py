from django.urls import path

from .views import (
    attendance_dashboard,
    class_attendance_view,
    monthly_attendance_grid,
    toggle_attendance,
    import_attendance_excel,
)

urlpatterns = [

    path(
        "",
        attendance_dashboard,
        name="attendance_dashboard",
    ),

    path(
        "class/<int:class_id>/",
        class_attendance_view,
        name="class_attendance",
    ),
    path(
    "monthly/<int:class_id>/",
    monthly_attendance_grid,
    name="monthly_attendance_grid",
    ),
    path(
    "toggle/<int:class_id>/<int:student_id>/<int:year>/<int:month>/<int:day>/",
    toggle_attendance,
    name="toggle_attendance",
    ),
    path(
    "import/",
    import_attendance_excel,
    name="import_attendance_excel",
    ),

]