from django.contrib.auth import login
from django.views.generic import FormView
from rest_framework.reverse import reverse_lazy

from subscriptions.forms import StudentRegistrationWithPlanForm
from subscriptions.models import Plan
from subscriptions.services.subscription import subscription_create


class SubscriptionFormView(FormView):
    template_name = 'subscriptions/subscription_create.html'
    form_class = StudentRegistrationWithPlanForm
    success_url = reverse_lazy('course_list')
    extra_context = {
        'plans': Plan.objects.all()
    }

    def form_valid(self, form):
        student = form.save()
        plan = form.cleaned_data['plan']

        login(self.request, student)
        subscription_create(student, plan)

        return super().form_valid(form)
