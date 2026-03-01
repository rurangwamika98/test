from .models import AuditLog


class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.method == "GET" and request.path.startswith("/api/") and request.user.is_authenticated:
            AuditLog.objects.create(user=request.user, path=request.path, method=request.method)
        return response
