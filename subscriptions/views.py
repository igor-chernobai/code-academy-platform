from datetime import timedelta

from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.utils import timezone

from subscriptions.forms import StudentRegistrationWithPlanForm
from subscriptions.models import StudentSubscription, SubscriptionPlan


def subscription_create(request):
    if request.method == "POST":
        form = StudentRegistrationWithPlanForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            plan = form.cleaned_data["plan"]

            StudentSubscription.objects.create(student=user,
                                               plan=plan,
                                               end_date=timezone.now() + timedelta(plan.duration_days))
            return redirect("course_list")
    else:

        form = StudentRegistrationWithPlanForm()
        context = {"form": form, "plans": SubscriptionPlan.objects.all()}
        return render(request, "subscriptions/subscription_create.html", context)
