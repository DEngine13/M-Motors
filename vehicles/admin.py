from django.contrib import admin
from .models import Vehicle

# Register your models here.
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("brand", "model", "year", "mileage", "sale_price", "monthly_rental", "vehicle_type", "is_active")
    list_filter = ("vehicle_type", "is_active")
    list_editable = ("vehicle_type", "is_active")
