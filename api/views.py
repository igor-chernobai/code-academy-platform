from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from api.permissions import IsAdminOrReadOnly, IsEnrolled, HasActiveSubscription
from courses.models import Course, Lesson
from courses.serializers import CourseSerializer, LessonSerializer
from users.serializers import UserSerializer
from users.services.student_course import (get_lesson_for_student,
                                           updated_activity)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(methods=['post'],
            detail=True,
            permission_classes=[IsAuthenticated, HasActiveSubscription])
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        course.students.add(request.user)
        return Response({"course": course.title,
                         "enroll": True},
                        status=status.HTTP_201_CREATED)

    @action(methods=['get'],
            detail=False,
            permission_classes=[IsAuthenticated, HasActiveSubscription])
    def student_courses(self, request):
        serializer = self.get_serializer(Course.objects.filter(students=self.request.user), many=True)
        return Response({'student_courses': serializer.data},
                        status=status.HTTP_200_OK)


class StudentLessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, HasActiveSubscription, IsEnrolled]

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


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['is_staff', 'is_active']
    ordering_fields = ['id', 'email', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name']
