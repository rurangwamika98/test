from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from .validators import validate_nid, validate_rwanda_phone


class UserType(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    AGENT = "AGENT", "Agent"
    CUSTOMER = "CUSTOMER", "Customer"
    DRIVER = "DRIVER", "Driver"
    GOV = "GOV", "Government"


class User(AbstractUser):
    username = None
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=13, unique=True)
    user_type = models.CharField(max_length=20, choices=UserType.choices, default=UserType.CUSTOMER)
    nid_number = models.CharField(max_length=16, blank=True)
    assigned_sector = models.CharField(max_length=120, blank=True)
    is_verified = models.BooleanField(default=False)
    tos_version = models.CharField(max_length=20, default="v1")

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def clean(self):
        if not validate_rwanda_phone(self.phone):
            raise ValidationError({"phone": "Phone must match +2507XXXXXXXX"})
        if self.nid_number and not validate_nid(self.nid_number):
            raise ValidationError({"nid_number": "Invalid Rwanda NID format."})
