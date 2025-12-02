from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View, generic

from courses.models import Course, Lesson
from users import forms as student_forms
from users.models import StudentLastActivity, StudentProgress
from users.services.user_lessons import get_last_student_lesson

from .mixins import StudentCourseAccessMixin


class UserLoginView(LoginView):
    form_class = student_forms.UserLoginForm
    template_name = "users/user_login.html"


class UserRegisterView(generic.CreateView):
    form_class = student_forms.UserRegisterForm
    template_name = "users/user_registration.html"
    success_url = reverse_lazy("courses")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        login(self.request, user)
        return response


class StudentEnrollCourseView(LoginRequiredMixin, generic.FormView):
    course = None
    form_class = student_forms.CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data["course"]

        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("users:student_course", args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin, generic.ListView):
    model = Course
    template_name = "users/student_courses.html"
    context_object_name = "courses"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students=self.request.user).annotate(count_modules=Count("modules", distinct=True),
                                                              count_lessons=Count("modules__lessons"))


class StudentLessonDetailView(LoginRequiredMixin, StudentCourseAccessMixin, generic.DetailView):
    model = Lesson
    template_name = "users/student_lesson.html"
    slug_url_kwarg = "lesson_slug"

    def get_object(self, queryset=None):
        lesson_slug = self.kwargs.get("lesson_slug", None)

        if lesson_slug:
            lesson = get_object_or_404(Lesson.objects.select_related("module__course"),
                                       slug=lesson_slug,
                                       module__course=self.course)
        else:
            lesson = get_last_student_lesson(student=self.request.user, course=self.course)

        return lesson

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        StudentLastActivity.objects.update_or_create(student=self.request.user,
                                                     course=self.course,
                                                     defaults={"last_lesson": self.object})

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
