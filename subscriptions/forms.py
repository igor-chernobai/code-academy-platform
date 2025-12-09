from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from subscriptions.models import SubscriptionPlan


class StudentRegistrationWithPlanForm(UserCreationForm):
    plan = forms.ModelChoiceField(widget=forms.RadioSelect,
                                  queryset=SubscriptionPlan.objects.all())
    first_name = forms.CharField(label="Ім'я",
                                 widget=forms.TextInput(attrs={
                                     "class": "input"}))

    class Meta:
        model = get_user_model()
        fields = ["email", "first_name", "plan"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget = forms.EmailInput(attrs={"class": "input"})
        self.fields['password1'].widget = forms.PasswordInput(attrs={"class": "input"})
        self.fields['password2'].widget = forms.PasswordInput(attrs={"class": "input"})
