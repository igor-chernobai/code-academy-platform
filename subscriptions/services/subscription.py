from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from subscriptions.models import Subscription, SubscriptionPlan

UserModel = get_user_model()


def subscription_create(student: UserModel, plan: SubscriptionPlan) -> Subscription:
    end_date = timezone.now() + timedelta(plan.duration_days)

    subscription = Subscription.objects.create(student=student,
                                               plan=plan,
                                               end_date=end_date)

    return subscription
