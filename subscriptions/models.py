from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class SubscriptionPlan(models.Model):
    name = models.CharField("назва", max_length=50, unique=True)
    price = models.PositiveIntegerField("ціна", unique=True)
    features = models.TextField("переваги")
    duration_days = models.PositiveIntegerField("інтервал плану")

    def __str__(self):
        return f"{self.name.title()} (Ціна: {self.price}, інтервал: {self.duration_days})"


class StudentSubscription(models.Model):
    student = models.ForeignKey(get_user_model(),
                                on_delete=models.CASCADE,
                                verbose_name="студент")
    plan = models.ForeignKey(SubscriptionPlan,
                             on_delete=models.CASCADE,
                             verbose_name="план")
    start_date = models.DateTimeField("дата покупки",
                                      auto_now=True)
    end_date = models.DateTimeField("дата покупки", blank=True)

    @property
    def is_active(self):
        return self.end_date >= timezone.now()

    def __str__(self):
        return f"{self.student} | {self.plan} | {self.is_active}"
