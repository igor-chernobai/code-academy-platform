from rest_framework import serializers

from subscriptions.models import Plan, Subscription
from subscriptions.services.subscription import subscription_update
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
    student = serializers.HiddenField(default=serializers.CurrentUserDefault())
    student_data = UserShortSerializer(source='student', read_only=True)
    plan = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Plan.objects.all())
    plan_data = PlanShortSerializer(source='plan', read_only=True)
    start_date = serializers.DateTimeField(format='%d.%m.%Y %H:%M', read_only=True)
    end_date = serializers.DateTimeField(format='%d.%m.%Y %H:%M', read_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'student', 'student_data', 'plan', 'plan_data', 'start_date', 'end_date', 'is_active']

    def validate(self, data):
        plan = data.get('plan', None)
        student = self.context['request'].user

        if plan is None:
            raise serializers.ValidationError({'plan': 'Виберіть план для підписки'})

        if plan == student.subscription.plan:
            raise serializers.ValidationError({'plan': 'План не може повторюватися зі старим'})

        return data

    def update(self, instance, validated_data):
        plan = validated_data.get('plan')
        instance.plan = plan
        instance.save()

        subscription_update(instance.student, plan)
        return instance
