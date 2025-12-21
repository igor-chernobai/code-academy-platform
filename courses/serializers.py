from rest_framework import serializers

from courses.models import Course


class CourseSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'created', 'owner', 'about']

    def create(self, validated_data):
        return Course.objects.create(**validated_data)
