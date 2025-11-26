from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserLoginForm, UserRegisterForm
from django.contrib.auth.views import LoginView


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "users/user_login.html"

class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "users/user_registration.html"
    success_url = reverse_lazy("courses")
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        login(self.request, user)
        return response
