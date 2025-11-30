from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect

from courses.models import Course, Lesson, LessonProgress
from courses.services.student_course_enroll import is_student_enrolled
from users.forms import CourseEnrollForm


def courses_page(request):
    courses = Course.objects.annotate(count_modules=Count("modules"),
                                      count_lessons=Count("modules__lessons")
                                      )
    return render(request, "courses/courses.html", {"courses": courses})


def course_detail(request, slug):
    course = get_object_or_404(Course.objects.prefetch_related("modules"), slug=slug)

    enroll_form = CourseEnrollForm(initial={"course": course})
    context = {"course": course, "enroll_form": enroll_form,
               "is_student_enrolled": is_student_enrolled(course, request.user)}
    return render(request, "courses/detail.html", context)


@login_required
def lesson_detail(request, slug):
    lesson = get_object_or_404(Lesson.objects.select_related("module__course"), slug=slug)
    course = lesson.module.course
    course = Course.objects.prefetch_related("modules__lessons").get(id=course.id)

    if  not is_student_enrolled(course, request.user):
        return redirect("courses:course_detail", slug=course.slug)

    context = {"course": course, "lesson": lesson}
    return render(request, "courses/lesson.html", context)


def lesson_complete(request, slug):
    lesson = get_object_or_404(Lesson, slug=slug)
    if request.method == "POST":
        LessonProgress.objects.create(student=request.user,
                                      lesson=lesson,
                                      is_complete=True)

        next_lesson = lesson.get_next
        if next_lesson:
            return redirect("courses:lesson", next_lesson.slug)
        else:
            return redirect("courses")
