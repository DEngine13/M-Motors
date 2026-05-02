from django.db import models

# Creates Model for vehicles


class Vehicle(models.Model):
    SALE = "sale"
    RENTAL = "rental"
    BOTH = "both"
    TYPE_CHOICES = [
        (SALE, "For sale"),
        (RENTAL, "To rent"),
        (BOTH, "Buy or rent")
    ]

    brand = models.CharField("Brand", max_length=100)
    model = models.CharField("Model", max_length=100)
    year = models.PositiveIntegerField("Year")
    mileage = models.PositiveIntegerField("Mileage (km)")
    sale_price = models.DecimalField("Price (€)", max_digits=10, decimal_places=2, null=True, blank=True)
    monthly_rental = models.DecimalField("Monthly fee (€/month)", max_digits=8, decimal_places=2, null=True, blank=True)
    vehicle_type = models.CharField("Offer type", max_length=10, choices=TYPE_CHOICES, default=BOTH)
    description = models.TextField("Description", blank=True)
    photo = models.ImageField("Photo", upload_to="vehicles/", blank=True, null=True)
    is_active = models.BooleanField("Active", default=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"

    @property
    def is_for_sale(self):
        return self.vehicle_type in (self.SALE, self.BOTH)

    @property
    def is_for_rental(self):
        return self.vehicle_type in (self.RENTAL, self.BOTH)


class RentalOption(models.Model):
    name = models.CharField("Name", max_length=100)
    description = models.TextField("Description")
    monthly_price = models.DecimalField("Monthly price (€)", max_digits=8, decimal_places=2)
    is_active = models.BooleanField("Active", default=True)

    def __str__(self):
        return f"{self.name} ({self.monthly_price} €/month)"
