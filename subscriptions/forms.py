from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from subscriptions.models import SubscriptionPlan


class StudentRegistrationWithPlanForm(UserCreationForm):
    plan = forms.ModelChoiceField(widget=forms.RadioSelect,
                                  queryset=SubscriptionPlan.objects.all())
    username = forms.CharField(label="Ім'я студента",
                               widget=forms.TextInput(attrs={
                                   "class": "input"}))
    first_name = forms.CharField(label="Ім'я",
                                 widget=forms.TextInput(attrs={
                                     "class": "input"}))
    password1 = forms.CharField(label="Пароль",
                                widget=forms.PasswordInput(attrs={
                                    "class": "input"}))
    password2 = forms.CharField(label="Повторіть пароль",
                                widget=forms.PasswordInput(attrs={
                                    "class": "input"}))

    class Meta:
        model = get_user_model()
        fields = ["username", "first_name", "password1", "password2"]
