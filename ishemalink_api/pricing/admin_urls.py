from django.urls import path
from .views import clear_tariffs_cache

urlpatterns = [
    path("cache/clear-tariffs/", clear_tariffs_cache),
]
