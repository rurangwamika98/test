from django.urls import path
from .views import assign_role, list_roles

urlpatterns = [
    path("roles/", list_roles),
    path("assign/", assign_role),
]
