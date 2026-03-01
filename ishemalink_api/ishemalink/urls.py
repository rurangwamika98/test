from django.contrib import admin
from django.db import connection
from django.urls import include, path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


@api_view(["GET"])
@permission_classes([AllowAny])
def api_root(request):
    return Response({"name": "IshemaLink API", "version": "1.0.0", "status": "/api/status/"})


@api_view(["GET"])
@permission_classes([AllowAny])
def status_view(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        database = "ok"
    except Exception:
        database = "error"
    return Response({"status": "ok", "database": database})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api_root),
    path("api/status/", status_view),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/auth/", include("identity.auth_urls")),
    path("api/identity/", include("identity.urls")),
    path("api/users/", include("core.user_urls")),
    path("api/shipments/", include("domestic.urls")),
    path("api/pricing/", include("pricing.urls")),
    path("api/admin/", include("pricing.admin_urls")),
    path("api/privacy/", include("privacy.urls")),
    path("api/compliance/", include("privacy.compliance_urls")),
    path("api/rbac/", include("rbac.urls")),
    path("api/gov/", include("gov.urls")),
    path("api/analytics/", include("analytics.urls")),
    path("api/payments/", include("payments.urls")),
    path("api/notifications/", include("notifications.urls")),
    path("api/admin/dashboard/summary/", include("core.ops_urls")),
    path("api/health/deep/", include("core.health_urls")),
]
