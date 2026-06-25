from rest_framework.routers import DefaultRouter

from .views import (
    AssignmentViewSet,
    CourseViewSet,
    ProgramViewSet,
    SubmissionViewSet,
    TutoringAppointmentViewSet,
)

router = DefaultRouter()
router.register("programs", ProgramViewSet, basename="program")
router.register("courses", CourseViewSet, basename="course")
router.register("assignments", AssignmentViewSet, basename="assignment")
router.register("submissions", SubmissionViewSet, basename="submission")
router.register("tutoring-appointments", TutoringAppointmentViewSet, basename="tutoringappointment")

urlpatterns = router.urls
