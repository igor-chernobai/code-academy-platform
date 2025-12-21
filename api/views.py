from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from courses.models import Course
from courses.serializers import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(methods=['post'],
            detail=True)
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        course.students.add(request.user)
        return Response({"course": course.title,
                         "enroll": True})

