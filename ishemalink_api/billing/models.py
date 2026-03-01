from django.db import models


class Payment(models.Model):
    shipment_ref = models.CharField(max_length=40)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, default="PENDING")
    provider = models.CharField(max_length=20, default="MOMO")
