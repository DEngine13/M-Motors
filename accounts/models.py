from django.contrib.auth.models import AbstractUser
from django.db import models

# User inherits from the AbstractUser class and adds phone and address
class User(AbstractUser):
    phone = models.CharField("Phone", max_length=20, blank=True)
    address = models.TextField("Address", blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"