from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

# On fait hériter User de la classe AbstractUser pour lui assigner un téléphone et une adresse
class User(AbstractUser):
    phone = models.CharField("Phone", max_length=20, blank=True)
    address = models.TextField("Address", blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"