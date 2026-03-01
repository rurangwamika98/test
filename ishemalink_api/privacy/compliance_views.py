from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import AuditLog


@api_view(["GET"])
def audit_logs(request):
    data = list(AuditLog.objects.values("id", "path", "method", "created_at")[:200])
    return Response(data)
