from django.contrib.auth import get_user_model
from rest_framework import serializers

from courses.models import Course, Lesson


class CourseOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email"]


class CourseListSerializer(serializers.ModelSerializer):
    count_modules = serializers.ReadOnlyField()
    count_lessons = serializers.ReadOnlyField()
    count_students = serializers.ReadOnlyField()
    owner_data = CourseOwnerSerializer(source="owner", read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "slug",
            "short_description",
            "image",
            "owner_data",
            "count_modules",
            "count_lessons",
            "count_students",
            "created",
        ]


class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "title", "slug", "short_description", "about", "image", "created"]


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
