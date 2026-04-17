from django.urls import path
from . import views

app_name = "vehicles"

# App's root "/" sends vehicle list
urlpatterns = [
    path("", views.vehicle_list, name="vehicle_list"),
    path("vehicule/<int:pk>", views.vehicle_detail, name="vehicle_detail"),
    path("rental-options/", views.rental_options_page, name="rental_options"),
]