from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views import generic

from courses.models import Course
from users.forms import CourseEnrollForm
from users.services.student_course_enroll import is_student_enrolled


class CourseListView(generic.ListView):
    template_name = "courses/course_list.html"
    queryset = Course.objects.annotate(count_modules=Count("modules", distinct=True),
                                       count_lessons=Count("modules__lessons"))
    context_object_name = "course_list"


class CourseDetailView(generic.DetailView):
    template_name = "courses/course_detail.html"

    def get_object(self, queryset=None):
        course = get_object_or_404(Course.objects.prefetch_related("modules"), slug=self.kwargs["slug"])
        return course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["enroll_form"] = CourseEnrollForm(initial={"course": self.object})
        context["is_student_enrolled"] = is_student_enrolled(self.object, self.request.user)
        return context
