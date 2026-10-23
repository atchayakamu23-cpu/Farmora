from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RegisterForm
from .models import Profile

def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )

            Profile.objects.create(
                user=user,
                role=form.cleaned_data["role"],
                phone=form.cleaned_data["phone"],
                address=form.cleaned_data["address"],
            )

            messages.success(request, "Registration successful. Please login.")
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect("home")

        messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")

@login_required
def user_logout(request):
    logout(request)
    return redirect("home")

@login_required
def profile(request):
    profile_data = get_object_or_404(Profile, user=request.user)
    return render(request, "accounts/profile.html", {"profile": profile_data})
