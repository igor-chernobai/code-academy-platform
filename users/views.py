from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from users.forms import UserLoginForm


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd["username"],
                                password=cd["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("courses")
    else:
        form = UserLoginForm()

    context = {"form": form}
    return render(request, "users/user_login.html", context)
