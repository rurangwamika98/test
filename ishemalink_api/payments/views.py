from decimal import Decimal

from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from domestic.models import Shipment
from .models import Payment, PaymentStatus
from .services import MomoMockAdapter


@api_view(["POST"])
def initiate_payment(request):
    shipment_ref = request.data.get("shipment_ref", "")
    phone = request.data.get("phone", request.user.phone)
    provider = request.data.get("provider", "MOMO")
    shipment = Shipment.objects.filter(tracking_code=shipment_ref).first()
    if shipment is None:
        return Response({"detail": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)

    adapter = MomoMockAdapter()
    gateway_payload = adapter.initiate_push(phone=phone, amount=Decimal(shipment.price_rwf), provider=provider)
    payment = Payment.objects.create(
        shipment_ref=shipment_ref,
        payer=request.user,
        phone=phone,
        amount=shipment.price_rwf,
        status=PaymentStatus.PENDING,
        provider=gateway_payload["provider"],
        external_reference=gateway_payload["external_reference"],
    )
    return Response(
        {
            "payment_id": payment.id,
            "shipment_ref": shipment_ref,
            "status": payment.status,
            "external_reference": payment.external_reference,
        },
        status=status.HTTP_202_ACCEPTED,
    )


@api_view(["POST"])
def payment_webhook(request):
    external_reference = request.data.get("external_reference", "")
    incoming_status = request.data.get("status", "FAILED").upper()
    payment = Payment.objects.filter(external_reference=external_reference).first()
    if payment is None:
        return Response({"detail": "Payment reference not found"}, status=status.HTTP_404_NOT_FOUND)

    if incoming_status not in {PaymentStatus.SUCCESS, PaymentStatus.FAILED}:
        return Response({"detail": "Invalid payment status"}, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        payment.status = incoming_status
        payment.save(update_fields=["status", "updated_at"])
        shipment = Shipment.objects.filter(tracking_code=payment.shipment_ref).first()
        if shipment:
            shipment.status = "IN_TRANSIT" if incoming_status == PaymentStatus.SUCCESS else "PENDING"
            shipment.save(update_fields=["status"])

    return Response({"payment": payment.external_reference, "status": payment.status})
