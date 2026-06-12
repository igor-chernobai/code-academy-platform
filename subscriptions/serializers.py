from rest_framework import serializers

from subscriptions.models import Plan, Subscription
from subscriptions.services.subscription import subscription_create


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ["id", "name", "price", "features", "duration_days"]


class SubscriptionWriteSerializer(serializers.ModelSerializer):
    student = serializers.HiddenField(default=serializers.CurrentUserDefault())
    plan = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Plan.objects.all())
    plan_data = PlanSerializer(source="plan", read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Subscription
        fields = ["id", "student", "plan_data", "plan", "start_date", "end_date", "is_active"]
        read_only_fields = ["start_date", "end_date"]

    def create(self, validated_data):
        student = validated_data["student"]
        plan = validated_data["plan"]

        subscription = subscription_create(student, plan)

        return subscription

    def validate(self, data):
        if "plan" not in data:
            raise serializers.ValidationError("Plan is required")
        return data


class SubscriptionReadSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Subscription
        fields = ["id", "plan", "start_date", "end_date", "is_active"]
