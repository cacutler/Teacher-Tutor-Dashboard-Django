import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class Status(models.Model):
    """
    Tag-style status a user can hold (e.g. 'verified', 'on-leave', 'suspended').
    A user can have zero, one, or many of these at once.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "statuses"
        ordering = ["name"]

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.

    Inherited from AbstractUser (no need to redefine):
      - username, email, password (hashed automatically), first_name, last_name,
        is_active, is_staff, is_superuser, date_joined, last_login, groups, permissions

    Added below to match the spec:
      - id as UUID (overrides AbstractUser's default integer pk)
      - middle_name, birthdate, gender
      - statuses (M2M tag field, replacing the "Status" list-of-strings)

    NOT added as fields (these are reverse relations, available automatically once
    the related models below define their ForeignKeys):
      - Assignment Submissions  -> user.submissions.all()
      - Tutoring Appointments   -> user.tutoring_as_tutor.all() / user.tutoring_as_tutee.all()
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    middle_name = models.CharField(max_length=150, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=50, blank=True)
    statuses = models.ManyToManyField(
        Status,
        blank=True,
        related_name="users",
    )

    def __str__(self):
        return self.username
