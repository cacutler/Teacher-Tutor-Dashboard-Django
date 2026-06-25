from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from .models import Assignment, Course, Program, Submission, TutoringAppointment
from .serializers import (
    AssignmentSerializer,
    CourseSerializer,
    ProgramSerializer,
    SubmissionSerializer,
    TutoringAppointmentSerializer,
)


class IsTeacherOrReadOnly(permissions.BasePermission):
    """
    Anyone authenticated can read. Only the owning teacher (or staff) can
    write. Works for Program/Assignment (real teacher FK) and Course
    (teacher is a derived property from course.program.teacher) alike,
    since we compare the related object rather than assuming a column.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_staff:
            return True
        return obj.teacher == request.user


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.select_related("teacher").order_by("title")
    serializer_class = ProgramSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related("program", "program__teacher").order_by("title")
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrReadOnly]

    def perform_create(self, serializer):
        # program is supplied by the client; confirm the requester actually
        # teaches that program before allowing the course to be created under it.
        program = serializer.validated_data["program"]
        if not self.request.user.is_staff and program.teacher_id != self.request.user.id:
            raise PermissionDenied("You don't teach this program.")
        serializer.save()


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.select_related("teacher", "course").order_by("title")
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class SubmissionViewSet(viewsets.ModelViewSet):
    """
    Students: only ever see/create/update their own submissions.
    Teachers: see submissions for assignments they created. Staff: see all.
    """
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Submission.objects.select_related("assignment", "student").order_by("-submitted_at")
        if user.is_staff:
            return qs
        return qs.filter(student=user) | qs.filter(assignment__teacher=user)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class TutoringAppointmentViewSet(viewsets.ModelViewSet):
    """Visible only to the tutor, the tutee, or staff."""
    serializer_class = TutoringAppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = TutoringAppointment.objects.select_related("tutor", "tutee", "course").order_by("title")
        if user.is_staff:
            return qs
        return qs.filter(tutor=user) | qs.filter(tutee=user)

    def perform_create(self, serializer):
        serializer.save(tutor=self.request.user)
