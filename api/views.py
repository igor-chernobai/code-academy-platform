from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import mixins

from api.permissions import HasActiveSubscription, IsEnrolled
from courses.models import Course, Lesson
from courses.serializers import CourseListSerializer, LessonSerializer
from courses.services import CourseService
from subscriptions.models import Plan, Subscription
from subscriptions.serializers import (
    PlanSerializer,
    SubscriptionReadSerializer,
    SubscriptionWriteSerializer,
)

# from subscriptions.services.subscription import subscription_update
from users.serializers import LessonCompleteSerializer, UserRegisterSerializer, UserUpdateSerializer
from users.services.student_course import (
    complete_lesson,
    get_first_uncompleted_lesson,
    get_lesson_by_slug,
)


class CourseViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CourseListSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["created", "count_students"]
    search_fields = ["title"]

    def get_queryset(self):
        return CourseService.get_courses_with_stats()


class StudentLessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, HasActiveSubscription, IsEnrolled]

    def get_object(self):
        course_id = self.kwargs.get("course_id")
        lesson_slug = self.kwargs.get("slug")

        if lesson_slug:
            lesson = get_lesson_by_slug(course_id=course_id, lesson_slug=lesson_slug)
        else:
            lesson = get_first_uncompleted_lesson(course_id=course_id, student=self.request.user)

        course = get_object_or_404(Course, id=course_id)
        self.check_object_permissions(self.request, course)

        return lesson


class UserCreate(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserRegisterSerializer


class UserMeAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionWriteSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]


class SubscriptionRetrieveAPIVIew(generics.RetrieveAPIView):
    serializer_class = SubscriptionReadSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Subscription, student=self.request.user)


class PlanListAPIView(generics.ListAPIView):
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()


class SubscriptionUpdateAPIView(generics.UpdateAPIView):
    serializer_class = SubscriptionWriteSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        subscription = get_object_or_404(Subscription, student=self.request.user)
        self.check_object_permissions(self.request, subscription)
        return subscription

    # def perform_update(self, serializer):
    #     student = self.get_object().student
    #     plan = serializer.validated_data["plan"]

    # serializer.instance = subscription_update(student, plan)


class LessonCompleteAPIView(APIView):
    permission_classes = [IsAuthenticated, HasActiveSubscription]

    @extend_schema(
        request=None,
        responses=LessonCompleteSerializer,
        summary="Complete lesson",
        description="Marks lesson as completed for authenticated student",
    )
    def post(self, request, lesson_id, format=None):
        progress = complete_lesson(request.user, lesson_id)
        serializer = LessonCompleteSerializer(progress)

        return Response(serializer.data, status=status.HTTP_200_OK)
