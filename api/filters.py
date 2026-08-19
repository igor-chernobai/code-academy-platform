from django_filters import FilterSet, NumberFilter

from courses.models import Course


class CourseFilter(FilterSet):
    min_students = NumberFilter(method="filter_min_students")

    def filter_min_students(self, queryset, name, value):
        return queryset.filter(students_count__gte=value)

    class Meta:
        model = Course
        fields = []
