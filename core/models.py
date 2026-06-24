import uuid

from django.conf import settings
from django.db import models

# settings.AUTH_USER_MODEL is used instead of importing accounts.User directly.
# This is the standard Django pattern for referencing the user model from other
# apps -- it avoids circular imports and respects whatever user model is active.


class Program(models.Model):
    """
    NOT a field here: "Courses" (list of course UUIDs). Once Course.program is
    defined below, this is available automatically as program.courses.all()
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="programs_taught",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Course(models.Model):
    """
    NOT a field here: "Assignments" (list of assignment UUIDs). Once
    Assignment.course is defined below, this is available automatically as
    course.assignments.all()
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        related_name="courses",
    )
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    # Self-referential M2M: a course can have many prerequisite courses.
    # symmetrical=False because "A requires B" does not imply "B requires A".
    prerequisites = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="required_for",
    )
    @property
    def teacher(self):
        return self.program.teacher

    def __str__(self):
        return self.title


class TutoringAppointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tutor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tutoring_as_tutor",
    )
    tutee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tutoring_as_tutee",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tutoring_appointments",
    )
    title = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    report = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Assignment(models.Model):
    """
    NOT a field here: "Submissions" (list of submission UUIDs). Once
    Submission.assignment is defined below, this is available automatically as
    assignment.submissions.all()
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="assignments_created",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="assignments",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


def submission_upload_path(instance, filename):
    # e.g. submissions/<assignment_id>/<student_id>/<filename>
    return f"submissions/{instance.assignment_id}/{instance.student_id}/{filename}"


class Submission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    # File-only entry. Text submissions are uploaded as text files (e.g. .txt),
    # so no separate text column is needed.
    entry = models.FileField(upload_to=submission_upload_path)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # A student can only submit once per assignment. Remove this if you
        # want to allow multiple submission attempts per student.
        unique_together = ("assignment", "student")

    def __str__(self):
        return f"{self.student} -> {self.assignment}"
