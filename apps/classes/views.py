from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required,
)
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from apps.core.decorators import (
    role_required,
)

from .forms import (
    MoveStudentForm,
)
from .models import (
    Enrollment,
    SchoolClass,
)

@login_required
@role_required([
    "ADMIN",
    "TEACHER",
])
def remove_student_from_class(
    request,
    enrollment_id,
):

    enrollment = get_object_or_404(
        Enrollment,
        id=enrollment_id,
    )

    enrollment.is_active = False

    enrollment.save(
        update_fields=[
            "is_active",
            "updated_at",
        ]
    )

    messages.success(
        request,
        (
            f"{enrollment.student.full_name} "
            f"removed from "
            f"{enrollment.school_class.name}."
        ),
    )

    return redirect(
        "class_attendance",
        class_id=enrollment.school_class.id,
    )


@login_required
@role_required([
    "ADMIN",
    "TEACHER",
])
def move_student_to_class(
    request,
    enrollment_id,
):

    enrollment = get_object_or_404(
        Enrollment,
        id=enrollment_id,
    )

    if request.method == "POST":

        form = MoveStudentForm(
            request.POST
        )

        if form.is_valid():

            target_class = (
                form.cleaned_data[
                    "target_class"
                ]
            )

            # deactivate old enrollment
            enrollment.is_active = False

            enrollment.save(
                update_fields=[
                    "is_active",
                    "updated_at",
                ]
            )

            # create new enrollment
            Enrollment.objects.create(
                student=enrollment.student,
                school_class=target_class,
                is_active=True,
            )

            messages.success(
                request,
                (
                    f"{enrollment.student.full_name} "
                    f"moved to "
                    f"{target_class.name}."
                ),
            )

            return redirect(
                "class_attendance",
                class_id=target_class.id,
            )

    else:

        form = MoveStudentForm()

    return render(
        request,
        "classes/move_student.html",
        {
            "form": form,
            "enrollment": enrollment,
        },
    )