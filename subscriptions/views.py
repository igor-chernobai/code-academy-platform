from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.views.generic import CreateView, FormView
from rest_framework.reverse import reverse_lazy

from subscriptions.forms import (StudentRegistrationWithPlanForm,
                                 SubscriptionChangeForm)
from subscriptions.models import Plan
from subscriptions.services.subscription import (subscription_create,
                                                 subscription_update)


class SubscriptionCreateView(CreateView):
    template_name = 'subscriptions/subscription_create.html'
    form_class = StudentRegistrationWithPlanForm
    success_url = reverse_lazy('course_list')
    extra_context = {
        'plans': cache.get_or_set("plans", Plan.objects.all(), 60 * 5)
    }

    def form_valid(self, form):
        response = super().form_valid(form)
        plan = form.cleaned_data['plan']

        login(self.request, self.object)
        subscription_create(self.object, plan)

        return response


class SubscriptionChangeFormView(LoginRequiredMixin, FormView):
    form_class = SubscriptionChangeForm
    template_name = 'subscriptions/subscription_update.html'
    success_url = reverse_lazy('students:student_course_list')
    extra_context = {
        'plans': Plan.objects.all()
    }

    def form_valid(self, form):
        plan = form.cleaned_data['plan']
        subscription_update(self.request.user, plan)
        key = make_template_fragment_key('user_plans', [self.request.user.email])
        cache.delete(key)
        return super().form_valid(form)
