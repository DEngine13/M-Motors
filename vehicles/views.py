from django.shortcuts import render, get_object_or_404
from .models import Vehicle, RentalOption
import logging

logger = logging.getLogger(__name__)

# Gets the vehicle list


def vehicle_list(request):
    vehicles = Vehicle.objects.filter(is_active=True)

    # Filters
    brand = request.GET.get("brand", "")
    if brand:
        vehicles = vehicles.filter(brand__iexact=brand)

    vehicle_type = request.GET.get("type", "")
    if vehicle_type:
        if vehicle_type == "sale":
            vehicles = vehicles.filter(vehicle_type__in=["sale", "both"])
        elif vehicle_type == "rental":
            vehicles = vehicles.filter(vehicle_type__in=["rental", "both"])

    price_max = request.GET.get("price_max", "")
    if price_max:
        try:
            vehicles = vehicles.filter(sale_price__lte=int(price_max))
        except (ValueError, TypeError):
            pass

    km_max = request.GET.get("km_max", "")
    if km_max:
        try:
            vehicles = vehicles.filter(mileage__lte=int(km_max))
        except (ValueError, TypeError):
            pass

    all_brands = (
        Vehicle.objects.filter(is_active=True)
        .values_list("brand", flat=True)
        .distinct()
        .order_by("brand")
    )

    logger.info(
        "Catalog viewed: %d results (brand=%s, type=%s)",
        vehicles.count(), brand or "all", vehicle_type or "all",
    )

    return render(request, "vehicles/vehicle_list.html", {
        "vehicles": vehicles,
        "all_brands": all_brands,
        "current_brand": brand,
        "current_type": vehicle_type,
        "current_price_max": price_max,
        "current_km_max": km_max,
    })

# Retrieves a vehicle with its Primary Key (pk), otherwise displays 404 page


def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, is_active=True)
    logger.info("Vehicle detail viewed: %s (id=%s)", vehicle, vehicle.pk)
    return render(request, "vehicles/vehicle_details.html", {"vehicle": vehicle})

# Retrieves active options


def rental_options_page(request):
    options = RentalOption.objects.filter(is_active=True)
    return render(request, "vehicles/rental_options.html", {"options": options})
