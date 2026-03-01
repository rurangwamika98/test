import uuid
from decimal import Decimal
from typing import TypedDict


class PaymentRequest(TypedDict):
    external_reference: str
    provider: str
    amount: str
    status: str


class MomoMockAdapter:
    """Small adapter to simulate MTN/Airtel momo request creation."""

    def initiate_push(self, *, phone: str, amount: Decimal, provider: str = "MOMO") -> PaymentRequest:
        ref = f"momo_{uuid.uuid4().hex[:12]}"
        return {
            "external_reference": ref,
            "provider": provider,
            "amount": str(amount),
            "status": "PENDING",
        }
