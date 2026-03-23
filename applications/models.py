from django.conf import settings
from django.db import models
from vehicles.models import Vehicle

class Application(models.Model):
    PURCHASE = "purchase"
    RENTAL = "rental"
    TYPE_CHOICES = [
        (PURCHASE, "Buy a car"),
        (RENTAL, "Rent a car")
    ]

    PENDING = "pending"
    REVIEWING = "reviewing"
    APPROVED = "approved"
    REJECTED = "rejected"
    STATUS_CHOICES = [
        (PENDING, "Awaiting processing"),
        (REVIEWING, "In review"),
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
    ]

    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications",
    )

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.PROTECT,
        related_name="applications",
    )

    application_type = models.CharField("Type", max_length=10, choices=TYPE_CHOICES)
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default=PENDING)
    rejection_reason = models.TextField("Reason for refusal", blank=True)
    created_at = models.DateTimeField("Submission date", auto_now_add=True)

    def __str__(self):
        return f"File #{self.pk} — {self.get_application_type_display()} — {self.vehicle}"


