from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ("student", "Student"),
        ("faculty", "Faculty"),
        ("coordinator", "Coordinator")
    )
    enrolment_number = models.CharField(max_length=20, blank=True, null=True)
    user_type = models.CharField(
        max_length=30,
        blank=True, null=True,
        choices=USER_TYPE_CHOICES)
    semester = models.IntegerField(null=True, blank=True)
