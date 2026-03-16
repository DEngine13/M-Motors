from django.urls import path
from . import views

app_name = "vehicles"

# À la racine de l'application "/", on renvoie la liste de véhicules
urlpatterns = [
    path("", views.vehicle_list, name="vehicle_list"),
]