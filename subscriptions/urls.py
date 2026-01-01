from django.urls import path

from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('create/', views.SubscriptionCreateView.as_view(), name='subscription_create'),
    path('change/', views.SubscriptionChangeFormView.as_view(), name='subscription_change')
]
