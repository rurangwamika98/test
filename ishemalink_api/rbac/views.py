from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response

User = get_user_model()


@api_view(["GET"])
def list_roles(request):
    return Response(["ADMIN", "AGENT", "CUSTOMER", "DRIVER", "GOV"])


@api_view(["POST"])
def assign_role(request):
    user = User.objects.get(id=request.data.get("user_id"))
    user.user_type = request.data.get("role", "CUSTOMER")
    user.save(update_fields=["user_type"])
    return Response({"user_id": user.id, "role": user.user_type})
