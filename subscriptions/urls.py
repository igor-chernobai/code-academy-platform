from django.urls import path

from . import views

app_name = "subscriptions"

urlpatterns = [
    path("create/", views.SubscriptionFormView.as_view(), name="subscription_create"),
]
