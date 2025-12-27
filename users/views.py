from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (PasswordChangeDoneView,
                                       PasswordChangeView)
from django.core.cache import cache
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View, generic

from courses.models import Course, Lesson
from users import forms as student_forms
from users.forms import StudentPasswordChangeForm
from users.models import StudentProgress
from users.services.student_course import (get_course_for_student,
                                           get_lesson_for_student,
                                           updated_activity)


class StudentEnrollCourseView(LoginRequiredMixin, generic.FormView):
    course = None
    form_class = student_forms.CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data["course"]

        self.course.students.add(self.request.user)
        key = f"course_{self.course.slug}:{self.request.user.id}"
        cache.delete(key)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("users:student_course", args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin, generic.ListView):
    model = Course
    template_name = "users/student_courses.html"
    context_object_name = "courses"

    def get_queryset(self):
        key = f"courses_for_{self.request.user.id}"
        courses = cache.get(key)

        if courses is None:
            courses = super().get_queryset().filter(students=self.request.user).annotate(
                count_modules=Count("modules", distinct=True),
                count_lessons=Count("modules__lessons"))
            cache.set(key, courses, 300)
        return courses


class StudentLessonDetailView(LoginRequiredMixin, generic.DetailView):
    model = Lesson
    template_name = "users/student_lesson.html"
    slug_url_kwarg = "lesson_slug"
    course = None

    def get_object(self, queryset=None):
        course_id = self.kwargs.get("course_id", None)
        lesson_slug = self.kwargs.get("lesson_slug", None)
        student = self.request.user

        self.course = get_course_for_student(student, course_id)  # get course with cache
        lesson = get_lesson_for_student(student, self.course.id, lesson_slug)  # get lesson with cache

        return lesson

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        updated_activity(student=self.request.user,
                         course_id=self.course.id,
                         last_lesson_id=self.object.id)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course"] = self.course
        context["lesson_complete_form"] = student_forms.LessonCompleteForm(
            initial={"lesson": self.object, "course": self.course})
        return context


class LessonCompleteView(LoginRequiredMixin, View):
    form_class = student_forms.LessonCompleteForm
    lesson = None

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            lesson = cd["lesson"]

            StudentProgress.objects.get_or_create(student=request.user,
                                                  lesson=lesson,
                                                  defaults={"is_complete": True})
            next_lesson = lesson.get_next
            if next_lesson:
                return redirect("users:student_course_lesson", cd["course"].id, next_lesson.slug)
            return redirect("course_list")
        return redirect("course_list")


class StudentPasswordChangeView(PasswordChangeView):
    template_name = "users/templates/registration/password_change.html"
    form_class = StudentPasswordChangeForm
    success_url = reverse_lazy("course_list")


class StudentPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = "users/templates/registration/password_change_done.html"
