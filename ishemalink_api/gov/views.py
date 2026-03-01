from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def manifests(request):
    return Response({"mode": "read-only", "items": []})


@api_view(["GET"])
def verify_license(request, license_no: str):
    return Response({"license_no": license_no, "valid": True})


@api_view(["POST"])
def sign_receipt(request):
    return Response({"signature": "EBM-MOCK-SIGNATURE"})


@api_view(["POST"])
def generate_manifest(request):
    return Response({"xml": "<manifest><status>ok</status></manifest>"})
