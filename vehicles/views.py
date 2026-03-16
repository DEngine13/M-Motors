from django.shortcuts import render, get_object_or_404
from .models import Vehicle

# Create your views here.

# On renvoie la liste de tous les véhicules
def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, "vehicles/vehicle_list.html", {"vehicles": vehicles})

# On récupère un véhicule par sa primary key (pk), sinon on renvoie une page 404
def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    return render(request, "vehicles/vehicle_details.html", {"vehicle": vehicle})