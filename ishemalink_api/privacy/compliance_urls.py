from django.urls import path
from .compliance_views import audit_logs

urlpatterns = [
    path("audit-logs/", audit_logs),
]
