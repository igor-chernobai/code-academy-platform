from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.permissions import IsEnrolled
from courses.models import Course, Lesson
from courses.serializers import CourseSerializer, LessonSerializer
from users.services.student_course import (get_lesson_for_student,
                                           updated_activity)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(methods=['post'],
            detail=True,
            permission_classes=[IsAuthenticated])
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        course.students.add(request.user)
        return Response({"course": course.title,
                         "enroll": True},
                        status=status.HTTP_201_CREATED)

    @action(methods=['get'],
            detail=False,
            permission_classes=[IsAuthenticated])
    def student_courses(self, request):
        return Response({'student_courses': Course.objects.filter(students=self.request.user).values()},
                        status=status.HTTP_200_OK)


class StudentLessonRetrieveAPIView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsEnrolled]

    def get_object(self):
        course_id = self.kwargs.get('course_id')
        lesson_slug = self.kwargs.get('slug')

        lesson = get_lesson_for_student(self.request.user,
                                        course_id,
                                        lesson_slug)

        updated_activity(student=self.request.user,
                         course_id=course_id,
                         last_lesson_id=lesson.id)
        return lesson
