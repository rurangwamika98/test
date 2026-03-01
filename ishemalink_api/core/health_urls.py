from django.urls import path

from .ops_views import deep_health

urlpatterns = [
    path("", deep_health),
]
