from users.forms import UserLoginForm
from django.contrib.auth.views import LoginView


class UserLogin(LoginView):
    form_class = UserLoginForm
    template_name = "users/user_login.html"
