from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Assignment, Course, Program, Submission, TutoringAppointment

User = get_user_model()


class MinimalUserSerializer(serializers.ModelSerializer):
    """Lightweight nested representation -- avoids leaking full user fields
    (email, birthdate, etc.) into every Program/Course/Assignment payload."""

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name"]


class ProgramSerializer(serializers.ModelSerializer):
    teacher = MinimalUserSerializer(read_only=True)

    class Meta:
        model = Program
        fields = ["id", "teacher", "title", "description"]


class CourseSerializer(serializers.ModelSerializer):
    teacher = MinimalUserSerializer(read_only=True)
    program_title = serializers.CharField(source="program.title", read_only=True)
    prerequisites = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Course.objects.all(), required=False
    )

    class Meta:
        model = Course
        fields = [
            "id", "program", "program_title", "teacher", "title", "subject",
            "description", "prerequisites",
        ]


class AssignmentSerializer(serializers.ModelSerializer):
    teacher = MinimalUserSerializer(read_only=True)
    course_title = serializers.CharField(source="course.title", read_only=True)

    class Meta:
        model = Assignment
        fields = [
            "id", "teacher", "course", "course_title", "title", "description",
        ]


class SubmissionSerializer(serializers.ModelSerializer):
    student = MinimalUserSerializer(read_only=True)
    assignment_title = serializers.CharField(source="assignment.title", read_only=True)

    class Meta:
        model = Submission
        fields = [
            "id", "assignment", "assignment_title", "student", "entry",
            "submitted_at",
        ]
        read_only_fields = ["id", "student", "submitted_at"]


class TutoringAppointmentSerializer(serializers.ModelSerializer):
    tutor = MinimalUserSerializer(read_only=True)
    tutee = MinimalUserSerializer(read_only=True)
    tutee_id = serializers.PrimaryKeyRelatedField(
        source="tutee", queryset=User.objects.all(), write_only=True
    )

    class Meta:
        model = TutoringAppointment
        fields = [
            "id", "tutor", "tutee", "tutee_id", "course", "title", "notes",
            "report",
        ]
        read_only_fields = ["id", "tutor"]
