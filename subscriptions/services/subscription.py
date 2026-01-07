from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import F
from django.utils import timezone

from subscriptions.models import Plan, Subscription, SubscriptionHistory

UserModel = get_user_model()


def subscription_create(student: UserModel, plan: Plan | int) -> Subscription:
    end_date = timezone.now() + timedelta(days=plan.duration_days)
    subscription_data = {'student': student, 'plan': plan, 'end_date': end_date}

    subscription = Subscription.objects.create(**subscription_data)
    SubscriptionHistory.objects.create(**subscription_data)

    return subscription


def subscription_update(student: UserModel, plan: Plan | int) -> Subscription:
    Subscription.objects.filter(student=student).update(end_date=F("end_date") + timedelta(days=plan.duration_days),
                                                        plan=plan)

    subscription = Subscription.objects.get(student=student)
    subscription_data = {'student': student, 'plan': plan, 'end_date': subscription.end_date}
    SubscriptionHistory.objects.create(**subscription_data)

    return subscription
