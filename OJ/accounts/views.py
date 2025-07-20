from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import UserExtension


# Create your views here.
def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        college = request.POST.get("college")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, "accounts/register.html")

        user = User.objects.create_user(
            username=username, email=email, password=password
        )

        u_extension = UserExtension(user=user, college=college)
        u_extension.save()
        messages.success(request, "Registration successful!")
        return redirect("login")

    return render(request, "accounts/register.html")


def login_user(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me") == "on"

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Username does not exist")
            return redirect("login")
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Invalid password")
            return redirect("login")

        if remember_me:
            request.session.set_expiry(60 * 60 * 24 * 30)  # 30 days
        else:
            request.session.set_expiry(0)

        login(request, user)
        return redirect("dashboard")

    return render(request, "accounts/login.html")


def logout_user(request):
    logout(request)
    return redirect("login")
