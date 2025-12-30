from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from subscriptions.models import SubscriptionPlan


class StudentRegistrationWithPlanForm(UserCreationForm):
    plan = forms.ModelChoiceField(queryset=SubscriptionPlan.objects.all())
    first_name = forms.CharField(label="Ім'я")

    class Meta:
        model = get_user_model()
        fields = ["email"]
