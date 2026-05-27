from django.contrib.auth.mixins import UserPassesTestMixin


class TeacherRequiredMixin(
    UserPassesTestMixin
):

    def test_func(self):

        return (
            self.request.user.is_authenticated
            and
            self.request.user.role in [
                "ADMIN",
                "TEACHER",
            ]
        )


class StudentRequiredMixin(
    UserPassesTestMixin
):

    def test_func(self):

        return (
            self.request.user.is_authenticated
            and
            self.request.user.role == "STUDENT"
        )