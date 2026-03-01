from asgiref.sync import async_to_sync
from django.db import transaction
from rest_framework import filters, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from notifications.services import send_email, send_sms
from pricing.services import PriceCalculator
from .models import Shipment, ShipmentLog
from .serializers import ShipmentLogSerializer, ShipmentSerializer


async def process_status_update(shipment: Shipment, status: str) -> None:
    shipment.status = status
    shipment.save(update_fields=["status"])
    ShipmentLog.objects.create(shipment=shipment, status=status, note="Async status update")
    tasks = [send_sms(shipment.sender.phone, f"Shipment {shipment.tracking_code} is now {status}")]
    if shipment.sender.email:
        tasks.append(send_email(shipment.sender.email, "Shipment update", status))
    for task in tasks:
        try:
            await task
        except Exception:
            continue


class ShipmentListView(generics.ListAPIView):
    queryset = Shipment.objects.all().order_by("-id")
    serializer_class = ShipmentSerializer
    filterset_fields = ["status", "destination"]
    search_fields = ["tracking_code"]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]


@api_view(["POST"])
def create_shipment(request):
    serializer = ShipmentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    with transaction.atomic():
        shipment = serializer.save(sender=request.user)
        shipment.price_rwf = PriceCalculator().calculate(shipment.weight_kg, shipment.destination)
        shipment.save(update_fields=["price_rwf"])
        ShipmentLog.objects.create(shipment=shipment, status=shipment.status, note="Created")
    return Response(ShipmentSerializer(shipment).data, status=201)


@api_view(["POST"])
def update_status(request, pk: int):
    shipment = Shipment.objects.get(pk=pk)
    new_status = request.data.get("status", "IN_TRANSIT")
    async_to_sync(process_status_update)(shipment, new_status)
    return Response({"message": "Status processing started", "shipment": shipment.tracking_code})


@api_view(["POST"])
def batch_update(request):
    shipment_ids = request.data.get("shipment_ids", [])
    status = request.data.get("status", "IN_TRANSIT")
    for shipment in Shipment.objects.filter(id__in=shipment_ids):
        async_to_sync(process_status_update)(shipment, status)
    return Response({"message": f"Processing started for {len(shipment_ids)} shipments.", "task_id": "task_local_async", "status": "queued"})


@api_view(["GET"])
def tracking_history(request, pk: int):
    shipment = Shipment.objects.get(pk=pk)
    data = ShipmentLogSerializer(shipment.logs.all().order_by("-created_at"), many=True).data
    return Response(data)


@api_view(["GET"])
def live_tracking(request, tracking_code: str):
    return Response({"tracking_code": tracking_code, "lat": -1.9441, "lng": 30.0619, "source": "mock-gps"})
