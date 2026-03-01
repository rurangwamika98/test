from django.conf import settings
from django.db import models


class ShipmentStatus(models.TextChoices):
    PENDING = "PENDING"
    IN_TRANSIT = "IN_TRANSIT"
    DELIVERED = "DELIVERED"
    CLEARED_CUSTOMS = "CLEARED_CUSTOMS"


class Shipment(models.Model):
    tracking_code = models.CharField(max_length=32, unique=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    destination = models.CharField(max_length=120)
    shipment_type = models.CharField(max_length=20, default="DOMESTIC")
    status = models.CharField(max_length=20, choices=ShipmentStatus.choices, default=ShipmentStatus.PENDING)
    weight_kg = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    price_rwf = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class ShipmentLog(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name="logs")
    status = models.CharField(max_length=20)
    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
