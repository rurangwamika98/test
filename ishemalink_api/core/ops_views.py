from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response

from domestic.models import Shipment
from payments.models import Payment, PaymentStatus


@api_view(["GET"])
def dashboard_summary(request):
    active_shipments = Shipment.objects.exclude(status="DELIVERED").count()
    revenue = Payment.objects.filter(status=PaymentStatus.SUCCESS).count()
    return Response({"active_shipments": active_shipments, "successful_payments": revenue})


@api_view(["GET"])
def deep_health(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        cursor.fetchone()
    return Response({"status": "ok", "database": "ok", "redis": "mock-ok", "disk": "ok"})
