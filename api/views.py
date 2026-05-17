from django.contrib.auth import get_user_model
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.permissions import (HasActiveSubscription, IsAdminOrReadOnly,
                             IsEnrolled)
from courses.models import Course, Lesson
from courses.serializers import (CourseDetailSerializer, CourseListSerializer,
                                 LessonSerializer)
from subscriptions.serializers import SubscriptionSerializer
from users.serializers import UserListCreateSerializer, UserUpdateSerializer
from users.services.student_course import (get_lesson_for_student,
                                           updated_activity)


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer

        return CourseDetailSerializer

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
    def my_courses(self, request):
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


class UserCreate(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserListCreateSerializer


class UserMeAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class SubscriptionDetail(generics.RetrieveAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.subscription
