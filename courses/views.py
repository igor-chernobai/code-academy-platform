from django.core.cache import cache
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views import generic

from courses.models import Course
from users.forms import CourseEnrollForm
from users.services.student_course import is_student_enrolled


class CourseListView(generic.ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        courses = cache.get('courses')
        if courses is None:
            courses = super().get_queryset().annotate(count_modules=Count('modules', distinct=True),
                                                      count_lessons=Count('modules__lessons'))
            cache.set('courses', courses, 300)
        return courses


class AboutTemplateView(generic.TemplateView):
    template_name = 'about.html'


class CourseDetailView(generic.DetailView):
    template_name = 'courses/course_detail.html'

    def get_object(self, queryset=None):
        course_slug = self.kwargs['slug']
        key = f'course_{course_slug}'
        course = cache.get(key)

        if course is None:
            course = get_object_or_404(Course.objects.prefetch_related('modules'), slug=course_slug)
            cache.set(key, course, 60)

        return course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(initial={'course': self.object})

        user = self.request.user
        if user.is_authenticated:
            key = f'course_{self.kwargs['slug']}:{user.id}'
            is_enrolled = cache.get(key)
            if is_enrolled is None:
                is_enrolled = is_student_enrolled(self.object, user)
                cache.set(key, is_enrolled, 600)

            context['is_student_enrolled'] = is_enrolled
        return context
