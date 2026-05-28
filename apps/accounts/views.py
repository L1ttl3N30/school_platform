from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import (
    login_required,
)
from django.shortcuts import (
    redirect,
    render,
)

from apps.core.decorators import (
    role_required,
)

from .forms import (
    StudentImportForm,
    StudentSignupForm,
)
from .import_service import (
    StudentImportService,
)


def student_signup(request):

    if request.user.is_authenticated():

        return redirect("/")

    if request.method == "POST":

        form = StudentSignupForm(
            request.POST
        )

        if form.is_valid():

            user = form.save()

            login(
                request,
                user,
            )

            messages.success(
                request,
                "Account created successfully.",
            )

            return redirect("/")

    else:

        form = StudentSignupForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "accounts/signup.html",
        context,
    )


@login_required
@role_required([
    "ADMIN",
    "TEACHER",
])
def import_students(request):

    if request.method == "POST":

        form = StudentImportForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            result = (
                StudentImportService.import_students(
                    excel_file=request.FILES[
                        "excel_file"
                    ],
                    school_class=form.cleaned_data[
                        "school_class"
                    ],
                    default_password=form.cleaned_data[
                        "default_password"
                    ],
                )
            )

            print(result)

            messages.success(
                request,
                (
                    f"Created "
                    f"{result['created_count']} "
                    f"students. "
                    f"Skipped "
                    f"{result['skipped_count']} students."
                ),
            )

            MAX_DISPLAYED_ISSUES = 20

            for issue in result["issues"][
                :MAX_DISPLAYED_ISSUES
            ]:

                messages.warning(
                    request,
                    issue,
                )

            remaining = (
                len(result["issues"])
                - MAX_DISPLAYED_ISSUES
            )

            if remaining > 0:

                messages.warning(
                    request,
                    (
                        f"And {remaining} "
                        f"more issues..."
                    ),
                )

            return redirect(
                "import_students"
            )

    else:

        form = StudentImportForm()

    return render(
        request,
        "accounts/import_students.html",
        {
            "form": form,
        },
    )