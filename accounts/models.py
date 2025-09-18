from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = "student", "Student"
        INSTRUCTOR = "instructor", "Instructor"

    role = models.CharField(
        max_length=32,
        choices=Role.choices,
        default=Role.STUDENT,
        help_text="Distinguishes permissions for students vs instructors."
    )

    def is_student(self) -> bool:
        return self.role == self.Role.STUDENT

    def is_instructor(self) -> bool:
        return self.role == self.Role.INSTRUCTOR
