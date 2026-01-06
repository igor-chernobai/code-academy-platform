from django.contrib.auth import get_user_model
from rest_framework import serializers

from subscriptions.models import Plan, Subscription
from users.serializers import UserShortSerializer


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'price', 'features', 'duration_days']


class PlanShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'price', 'duration_days']


class SubscriptionSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(write_only=True, queryset=get_user_model().objects.all())
    plan = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Plan.objects.all())
    student_data = UserShortSerializer(source='student', read_only=True)
    plan_data = PlanShortSerializer(source='plan', read_only=True)
    start_date = serializers.DateTimeField(format='%d.%m.%Y %H:%M')
    end_date = serializers.DateTimeField(format='%d.%m.%Y %H:%M')

    class Meta:
        model = Subscription
        fields = ['id', 'student', 'student_data', 'plan', 'plan_data', 'start_date', 'end_date', 'is_active']
