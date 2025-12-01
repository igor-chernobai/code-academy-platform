from django.db.models import Count
from django.shortcuts import get_object_or_404, render

from courses.models import Course
from users.forms import CourseEnrollForm
from users.services.student_course_enroll import is_student_enrolled


def course_list(request):
    courses = Course.objects.annotate(count_modules=Count("modules"),
                                      count_lessons=Count("modules__lessons")
                                      )
    return render(request, "courses/course_list.html", {"courses": courses})


def course_detail(request, slug):
    course = get_object_or_404(Course.objects.prefetch_related("modules"), slug=slug)

    enroll_form = CourseEnrollForm(initial={"course": course})
    context = {"course": course, "enroll_form": enroll_form,
               "is_student_enrolled": is_student_enrolled(course, request.user)}
    return render(request, "courses/course_detail.html", context)
