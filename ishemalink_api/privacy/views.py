from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response

User = get_user_model()


@api_view(["GET"])
def my_data(request):
    return Response({"id": request.user.id, "phone": request.user.phone, "role": request.user.user_type})


@api_view(["POST"])
def anonymize(request):
    user = request.user
    user.first_name = "Redacted"
    user.last_name = "Redacted"
    user.phone = f"redacted-{user.id}"
    user.email = ""
    user.save(update_fields=["first_name", "last_name", "phone", "email"])
    return Response({"status": "anonymized"})


@api_view(["GET"])
def consent_history(request):
    return Response({"tos_version": request.user.tos_version})
