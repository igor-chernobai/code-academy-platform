from django.db.models import Count

from courses.models import Course


class CourseService:
    @staticmethod
    def get_courses_with_stats():
        return Course.objects.annotate(
            count_modules=Count("modules", distinct=True),
            count_lessons=Count("modules__lessons", distinct=True),
            count_students=Count("students", distinct=True),
        ).select_related("owner")
