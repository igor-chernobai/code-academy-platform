from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class SubscriptionPlan(models.Model):
    name = models.CharField("назва", max_length=50, unique=True)
    price = models.PositiveIntegerField("ціна", unique=True)
    features = models.TextField("переваги")
    duration_days = models.PositiveIntegerField("інтервал плану")

    def __str__(self):
        return self.name


class Subscription(models.Model):
    student = models.ForeignKey(get_user_model(),
                                on_delete=models.CASCADE,
                                related_name='subscriptions',
                                verbose_name="студент")
    plan = models.ForeignKey(SubscriptionPlan,
                             on_delete=models.CASCADE,
                             verbose_name="план")
    start_date = models.DateTimeField("дата покупки",
                                      auto_now_add=True)
    end_date = models.DateTimeField("дата завершення", blank=True)

    @property
    def is_active(self):
        return self.end_date >= timezone.now()

    def __str__(self):
        status = 'Активна' if self.is_active else 'Не активна'
        return f"{self.student} | {self.plan} | {status.capitalize()}"
