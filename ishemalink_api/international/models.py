from django.db import models


class CustomsDocument(models.Model):
    shipment_reference = models.CharField(max_length=40)
    tin = models.CharField(max_length=30)
    passport = models.CharField(max_length=20)
    destination_country = models.CharField(max_length=80)
