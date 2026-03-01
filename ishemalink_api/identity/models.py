from django.conf import settings
from django.db import models


class OTPCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    purpose = models.CharField(max_length=32)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
