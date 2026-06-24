from django.contrib import admin

from .models import Assignment, Course, Program, Submission, TutoringAppointment


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("title", "teacher")
    search_fields = ("title",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "program", "teacher", "subject")
    search_fields = ("title", "subject")
    filter_horizontal = ("prerequisites",)


@admin.register(TutoringAppointment)
class TutoringAppointmentAdmin(admin.ModelAdmin):
    list_display = ("title", "tutor", "tutee", "course")
    search_fields = ("title",)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "teacher")
    search_fields = ("title",)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("assignment", "student", "submitted_at")
    list_filter = ("assignment",)
