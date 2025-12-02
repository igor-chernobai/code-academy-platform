from django.shortcuts import redirect

from courses.models import Course
from users.services.student_course_enroll import is_student_enrolled


class StudentCourseAccessMixin:
    """Перевірка що студент записан на курс"""

    def dispatch(self, request, *args, **kwargs):
        course_id = self.kwargs["course_id"]
        self.course = Course.objects.prefetch_related("modules__lessons").get(id=course_id)

        if not is_student_enrolled(self.course, request.user):
            return redirect("courses:course_detail", slug=self.course.slug)
        return super().dispatch(request, *args, *kwargs)
