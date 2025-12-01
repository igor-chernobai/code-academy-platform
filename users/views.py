from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from courses.models import Lesson
from users.forms import UserLoginForm, UserRegisterForm, CourseEnrollForm
from django.contrib.auth.views import LoginView


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
        first_lesson = Lesson.objects.select_related("module__course").filter(module__course=self.course).first()
        return reverse_lazy("courses:lesson", args=[first_lesson.slug])
