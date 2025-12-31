from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from subscriptions.models import Plan, Subscription, SubscriptionHistory

UserModel = get_user_model()


def subscription_create(student: UserModel, plan: Plan) -> Subscription:
    end_date = timezone.now() + timedelta(plan.duration_days)
    subscription_data = {'student': student, 'plan': plan, 'end_date': end_date}

    subscription = Subscription.objects.create(**subscription_data)
    SubscriptionHistory.objects.create(**subscription_data)

    return subscription
