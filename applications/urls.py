from django.urls import path
from . import views

app_name = "applications"

urlpatterns = [
    path("apply/<int:vehicle_pk>/", views.apply_purchase, name="apply_purchase"),
]