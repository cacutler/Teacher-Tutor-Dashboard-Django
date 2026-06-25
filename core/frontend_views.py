from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Assignment, Course, Submission


@login_required
def dashboard(request):
    user = request.user
    context = {
        "programs_taught": user.programs_taught.all() if hasattr(user, "programs_taught") else [],
        "assignments_created": user.assignments_created.all() if hasattr(user, "assignments_created") else [],
        "my_submissions": user.submissions.select_related("assignment").all(),
        "tutoring_as_tutor": user.tutoring_as_tutor.select_related("tutee", "course").all(),
        "tutoring_as_tutee": user.tutoring_as_tutee.select_related("tutor", "course").all(),
    }
    return render(request, "core/dashboard.html", context)


@login_required
def course_list(request):
    courses = Course.objects.select_related("program", "program__teacher").all()
    return render(request, "core/course_list.html", {"courses": courses})


@login_required
def course_detail(request, pk):
    course = get_object_or_404(
        Course.objects.select_related("program", "program__teacher").prefetch_related("assignments"),
        pk=pk,
    )
    return render(request, "core/course_detail.html", {"course": course})


@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(
        Assignment.objects.select_related("course", "teacher"), pk=pk
    )
    is_teacher = assignment.teacher_id == request.user.id
    my_submission = None
    if not is_teacher:
        my_submission = Submission.objects.filter(
            assignment=assignment, student=request.user
        ).first()

    if request.method == "POST" and not is_teacher:
        entry = request.FILES.get("entry")
        if entry:
            submission, _ = Submission.objects.update_or_create(
                assignment=assignment,
                student=request.user,
                defaults={"entry": entry},
            )
            return redirect("assignment_detail", pk=pk)

    context = {
        "assignment": assignment,
        "is_teacher": is_teacher,
        "my_submission": my_submission,
        "submissions": (
            assignment.submissions.select_related("student").all() if is_teacher else None
        ),
    }
    return render(request, "core/assignment_detail.html", context)
