from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import StudentProgress

UserModel = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(label="Ім`я")
    password = serializers.CharField(label="Пароль", write_only=True)
    password2 = serializers.CharField(label="Повторіть пароль", write_only=True)

    class Meta:
        model = UserModel
        fields = ["email", "first_name", "password", "password2"]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password2": "Паролі не збігаються"})

        return data

    def create(self, validated_data):
        del validated_data["password2"]
        user = UserModel.objects.create_user(**validated_data)

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["email", "first_name", "last_name"]


class LessonCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProgress
        fields = ["lesson_id", "is_complete"]
