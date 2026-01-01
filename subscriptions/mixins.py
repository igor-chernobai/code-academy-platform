from django.shortcuts import redirect


class SubscriptionCheckMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.subscription.is_active:
            return redirect("subscriptions:subscription_change")

        return super().dispatch(request, *args, **kwargs)
