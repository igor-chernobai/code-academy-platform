from django.contrib import admin
from unfold.admin import ModelAdmin

from subscriptions.models import Subscription, SubscriptionPlan


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(ModelAdmin):
    list_display = ["name", "price", "duration_days"]
    compressed_fields = True


@admin.register(Subscription)
class SubscriptionAdmin(ModelAdmin):
    list_display = ["student", "plan", "start_date", "end_date", "is_active"]
    compressed_fields = True
    readonly_fields = ['start_date']
