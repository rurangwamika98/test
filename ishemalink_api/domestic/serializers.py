from rest_framework import serializers
from .models import Shipment, ShipmentLog


class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = ["id", "tracking_code", "destination", "status", "weight_kg", "shipment_type", "price_rwf"]


class ShipmentLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentLog
        fields = ["status", "note", "created_at"]
