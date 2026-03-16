from django.db import models

# Create your models here.

# On créé le modèle de données pour les véhicules
class Vehicle(models.Model):
    brand = models.CharField("Brand", max_length=100)
    model = models.CharField("Model", max_length=100)
    year = models.PositiveIntegerField("Year")
    mileage = models.PositiveIntegerField("Mileage (km)")
    sale_price = models.DecimalField("Price (€)", max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"
    
    