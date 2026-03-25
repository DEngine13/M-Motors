from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from vehicles.models import Vehicle
from .models import Application

@login_required
def apply_purchase(request, vehicle_pk):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_pk, is_active=True)

    if request.method == "POST":
        Application.objects.create(
            applicant=request.user,
            vehicle=vehicle,
            application_type=Application.PURCHASE,
        )
        return redirect("vehicles:vehicle_list")
    
    return render(request, "applications/apply_purchase.html", {"vehicle": vehicle})

@login_required
def apply_rental(request, vehicle_pk):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_pk, is_active=True)

    if request.method == "POST":
        duration = request.POST.get("rental_duration")
        Application.objects.create(
            applicant=request.user,
            vehicle=vehicle,
            application_type=Application.RENTAL,
            rental_duration=duration,
        )
        return redirect("vehicles:vehicle_list")
    
    return render(request, "applications/apply_rental.html", {
        "vehicle": vehicle,
        "duration_choices": Application.DURATION_CHOICES,
    })