from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
