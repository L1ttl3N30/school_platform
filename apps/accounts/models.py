from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    full_name = models.CharField(
        max_length=255,
        blank=True,
    )

    student_code = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
    )
    reference_number = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        db_index=True,
    )

    class Role(models.TextChoices):
        ADMIN = "ADMIN", _("Admin")
        TEACHER = "TEACHER", _("Teacher")
        STUDENT = "STUDENT", _("Student")

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
        db_index=True,
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )

    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
    )



    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ["username"]

    def is_teacher(self):
        return self.role == self.Role.TEACHER

    def is_student(self):
        return self.role == self.Role.STUDENT

    def is_admin(self):
        return self.role == self.Role.ADMIN
    def __str__(self):

        return (
            self.full_name
            or self.username
        )
