from django.db import models


class Tariff(models.Model):
    zone = models.CharField(max_length=20, unique=True)
    base_price = models.IntegerField()
    kg_rate = models.IntegerField(default=0)
