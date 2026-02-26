from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from unfold.contrib.forms.widgets import WysiwygWidget

from subscriptions.models import Plan, Subscription, SubscriptionHistory


@admin.register(Plan)
class PlanAdmin(ModelAdmin):
    list_display = ['name', 'price', 'duration_days']
    list_display_links = ['name', 'price']
    list_editable = ['duration_days']
    compressed_fields = True
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }


@admin.register(Subscription)
class SubscriptionAdmin(ModelAdmin):
    list_display = ['student', 'plan', 'start_date', 'end_date', 'get_status']
    list_display_links = ['student', 'plan']
    readonly_fields = ['start_date']
    fields = ['student', 'plan', 'start_date', 'end_date']

    compressed_fields = True

    @admin.display(description='Активна?', boolean=True)
    def get_status(self, obj):
        return obj.is_active


@admin.register(SubscriptionHistory)
class SubscriptionHistoryAdmin(ModelAdmin):
    list_display = ['student', 'plan', 'start_date', 'end_date', 'get_status']
    list_display_links = ['student', 'plan']
    readonly_fields = ['start_date']
    fields = ['student', 'plan', 'start_date', 'end_date']
    search_fields = ['student__email', 'plan__name']

    compressed_fields = True

    @admin.display(description='Активна?', boolean=True)
    def get_status(self, obj):
        return obj.is_active


class SubscriptionTabular(StackedInline):
    model = Subscription
    readonly_fields = ['start_date']
    tab = True


class SubscriptionHistoryTabular(TabularInline):
    model = SubscriptionHistory
    tab = True
    readonly_fields = ['end_date']
    extra = 0
