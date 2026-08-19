from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import F
from django.utils import timezone
from rest_framework.generics import get_object_or_404

from subscriptions.models import Plan, Subscription, SubscriptionHistory
from subscriptions.tasks import send_update_subscription_email, send_welcome_email

UserModel = get_user_model()


def subscription_create(student: UserModel, plan: Plan | int) -> Subscription:
    end_date = timezone.now() + timedelta(days=plan.duration_days)
    subscription_data = {"student": student, "plan": plan, "end_date": end_date}

    subscription = Subscription.objects.create(**subscription_data)
    SubscriptionHistory.objects.create(**subscription_data)

    send_welcome_email.delay_on_commit(subscription.id)

    return subscription


def subscription_update(student: UserModel, plan: Plan) -> Subscription:
    Subscription.objects.filter(student=student).update(
        end_date=F("end_date") + timedelta(days=plan.duration_days), plan=plan
    )

    subscription = Subscription.objects.get(student=student)
    subscription_data = {
        "student": student,
        "plan": plan,
        "end_date": subscription.end_date,
    }
    SubscriptionHistory.objects.create(**subscription_data)

    send_update_subscription_email.delay_on_commit(subscription.id)

    return subscription


class SubscriptionService:
    @staticmethod
    def get_subscription(student: UserModel) -> Subscription:
        return get_object_or_404(Subscription, student=student)
