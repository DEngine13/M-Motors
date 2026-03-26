from django.urls import path
from . import views

app_name = "applications"

urlpatterns = [
    path("apply/<int:vehicle_pk>/", views.apply_purchase, name="apply_purchase"),
    path("apply-rental/<int:vehicle_pk>", views.apply_rental, name="apply_rental"),
    path("<int:pk>/documents/", views.upload_documents, name="upload_documents"),
]