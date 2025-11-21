from django.shortcuts import render, get_object_or_404, redirect

from courses.models import Course, Lesson, LessonProgress


def courses_page(request):
    courses = Course.objects.all()
    return render(request, "courses/courses.html", {"courses": courses})


def course_detail(request):
    course = Course.objects.get(owner=request.user)
    context = {"course": course}
    return render(request, "courses/detail.html", context)


def lesson_detail(request, slug):
    lesson = get_object_or_404(Lesson, slug=slug)
    context = {"course": lesson.module.course, "lesson": lesson}
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
