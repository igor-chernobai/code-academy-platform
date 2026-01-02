from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class Plan(models.Model):
    name = models.CharField('назва', max_length=50, unique=True)
    price = models.PositiveIntegerField('ціна', unique=True)
    features = models.TextField('переваги')
    duration_days = models.PositiveIntegerField('інтервал плану')

    class Meta:
        db_table = 'plans'
        verbose_name = 'план'
        verbose_name_plural = 'плани'

    def __str__(self):
        return self.name


class SubscriptionCommonInfo(models.Model):
    plan = models.ForeignKey(Plan,
                             on_delete=models.CASCADE,
                             verbose_name='план')
    start_date = models.DateTimeField('дата покупки',
                                      auto_now_add=True)
    end_date = models.DateTimeField('дата завершення', blank=True)

    class Meta:
        abstract = True

    @property
    def is_active(self):
        return self.end_date >= timezone.now()

    def __str__(self):
        status = 'Активна' if self.is_active else 'Не активна'
        return f'{self.student} | {self.plan} | {status.capitalize()}'


class Subscription(SubscriptionCommonInfo):
    student = models.OneToOneField(get_user_model(),
                                   on_delete=models.CASCADE,
                                   verbose_name='студент')

    class Meta:
        db_table = 'subscriptions'
        verbose_name = 'підписка'
        verbose_name_plural = 'підписки'


class SubscriptionHistory(SubscriptionCommonInfo):
    student = models.ForeignKey(get_user_model(),
                                on_delete=models.CASCADE,
                                verbose_name='студент')

    class Meta:
        db_table = 'subscription_histories'
        verbose_name = 'історія підписки'
        verbose_name_plural = 'історія підписки'
