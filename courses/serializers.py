from rest_framework import serializers

from courses.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'created', 'owner']

    def create(self, validated_data):
        return Course.objects.create(**validated_data)
