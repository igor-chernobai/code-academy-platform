from django.contrib import admin
from unfold.admin import ModelAdmin

from subscriptions.models import StudentSubscription, SubscriptionPlan


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(ModelAdmin):
    list_display = ["name", "price", "duration_days"]
    compressed_fields = True


@admin.register(StudentSubscription)
class StudentSubscriptionAdmin(ModelAdmin):
    list_display = ["student", "plan", "start_date", "is_active"]
    compressed_fields = True
