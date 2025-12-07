from django.urls import path

from . import views

app_name = "subscriptions"

urlpatterns = [
    path("create/", views.subscription_create, name="subscription_create"),
]
