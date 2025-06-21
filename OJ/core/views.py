from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import UserExtension

# Create your views here.


def homepage(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "core/homepage.html")


@login_required 
def dashboard(request):
    return render(request, "core/dashboard.html")


def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_ext = get_object_or_404(UserExtension, user=user)
    context = {
        "user": user,
        "user_ext": user_ext,
    }
    return render(request, "core/profile.html", context)
