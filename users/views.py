from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from courses.models import Course, Lesson, LessonProgress
from users.forms import CourseEnrollForm, UserLoginForm, UserRegisterForm
from users.models import StudentLastActivity
from users.services.user_lessons import get_last_student_lesson

from .services.student_course_enroll import is_student_enrolled


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "users/user_login.html"


class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "users/user_registration.html"
    success_url = reverse_lazy("courses")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        login(self.request, user)
        return response


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data["course"]

        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("users:student_course", args=[self.course.id])


@login_required
def student_course_list(request):
    courses = Course.objects.filter(students=request.user).annotate(count_modules=Count("modules"),
                                                                    count_lessons=Count("modules__lessons"))
    context = {"courses": courses}
    return render(request, "users/student_courses.html", context)


@login_required
def student_course_lesson(request, course_id, lesson_slug=None):
    course = Course.objects.prefetch_related("modules__lessons").get(id=course_id)

    if not is_student_enrolled(course, request.user):
        return redirect("courses:course_detail", slug=course.slug)

    if lesson_slug:
        lesson = get_object_or_404(Lesson.objects.select_related("module__course"), slug=lesson_slug)
    else:
        lesson = get_last_student_lesson(student=request.user, course=course)

    StudentLastActivity.objects.update_or_create(student=request.user,
                                                 course=course,
                                                 defaults={"last_lesson": lesson})

    context = {"course": course, "lesson": lesson}
    return render(request, "users/student_lesson.html", context)


def lesson_complete(request, slug):
    lesson = get_object_or_404(Lesson.objects.select_related("module__course"), slug=slug)
    if request.method == "POST":
        LessonProgress.objects.create(student=request.user,
                                      lesson=lesson,
                                      is_complete=True)

        next_lesson = lesson.get_next
        if next_lesson:
            return redirect("users:student_course_lesson", next_lesson.module.course.id, next_lesson.slug)
        else:
            return redirect("course_list")
