from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import ModelForm

from subscriptions.models import Plan, Subscription


class StudentRegistrationWithPlanForm(UserCreationForm):
    plan = forms.ModelChoiceField(queryset=Plan.objects.all())
    first_name = forms.CharField(label="Ім'я")

    class Meta:
        model = get_user_model()
        fields = ["email"]


class SubscriptionChangeForm(ModelForm):
    class Meta:
        model = Subscription
        fields = ['plan']
        error_messages = {
            'plan': {'required': 'Оберіть, будь-ласка, план підписки'}
        }
