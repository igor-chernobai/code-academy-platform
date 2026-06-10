from celery import shared_task
from django.core.mail import send_mail

from subscriptions.models import Subscription


@shared_task
def send_welcome_email(subscription_id):
    subscription = Subscription.objects.get(id=subscription_id)

    send_mail(
        subject="Вашу підписку успішно активовано",
        message=(
            f"Вітаємо, {subscription.student.first_name}!\n\n"
            f"Вашу підписку на тариф «{subscription.plan.name}» успішно активовано.\n\n"
            f"Дата завершення доступу: {subscription.end_date:%d.%m.%Y}.\n\n"
            f"Дякуємо за вибір Code Academy.\n"
            f"Бажаємо приємного навчання та швидкого професійного розвитку!\n\n"
            f"З повагою,\n"
            f"Команда Code Academy"
        ),
        from_email="noreply@codeacademy.com",
        recipient_list=[subscription.student.email],
        fail_silently=False,
    )


@shared_task
def send_update_subscription_email(subscription_id):
    subscription = Subscription.objects.get(id=subscription_id)

    send_mail(
        subject="Вашу підписку успішно продовжено",
        message=(
            f"Вітаємо, {subscription.student.first_name}!\n\n"
            f"Вашу підписку на тариф «{subscription.plan.name}» успішно продовжено.\n\n"
            f"Нова дата закінчення доступу: "
            f"{subscription.end_date:%d.%m.%Y}.\n\n"
            f"Дякуємо, що продовжуєте навчання разом із Code Academy.\n"
            f"Бажаємо успіхів у навчанні та досягненні ваших цілей!\n\n"
            f"З повагою,\n"
            f"Команда Code Academy"
        ),
        from_email="noreply@codeacademy.com",
        recipient_list=[subscription.student.email],
        fail_silently=False,
    )
