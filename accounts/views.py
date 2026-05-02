from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("vehicles:vehicle_list")
    else:
        form = SignUpForm()

    return render(request, "accounts/signup.html", {"form": form})


def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("vehicles:vehicle_list")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/signin.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("vehicles:vehicle_list")


@login_required
def profile(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get("first_name", "")
        user.last_name = request.POST.get("last_name", "")
        user.phone = request.POST.get("phone", "")
        user.address = request.POST.get("address", "")
        user.save()
        return redirect("accounts:profile")
    return render(request, "accounts/profile.html")


@login_required
def dashboard(request):
    applications = request.user.applications.all().order_by("-created_at")
    return render(request, "accounts/dashboard.html", {"applications": applications})
