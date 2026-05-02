from django.contrib import admin
from .models import Vehicle, RentalOption

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("brand", "model", "year", "mileage", "sale_price", "monthly_rental", "vehicle_type", "is_active")
    list_filter = ("vehicle_type", "is_active", "brand")
    search_fields = ("brand", "model")
    list_editable = ("vehicle_type", "is_active")
    actions = ["toggle_to_sale", "toggle_to_rental", "deactivate", "activate"]

    @admin.action(description="Toggle to Sale")
    def toggle_to_sale(self, request, queryset):
        count = queryset.update(vehicle_type=Vehicle.SALE)
        self.message_user(request, f"{count} vehicle(s) set to Sale.")

    @admin.action(description="Toggle to Rental")
    def toggle_to_rental(self, request, queryset):
        count = queryset.update(vehicle_type=Vehicle.RENTAL)
        self.message_user(request, f"{count} vehicle(s) set to Rental.")

    @admin.action(description="Deactivate selected vehicles")
    def deactivate(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"{count} vehicle(s) deactivated.")

    @admin.action(description="Activate selected vehicles")
    def activate(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f"{count} vehicle(s) activated.")

@admin.register(RentalOption)
class RentalOptionAdmin(admin.ModelAdmin):
    list_display = ("name", "monthly_price", "is_active")
    list_editable = ("is_active",)