from django.urls import path
from .views import calculate_view, tariffs_view

urlpatterns = [
    path("tariffs/", tariffs_view),
    path("calculate/", calculate_view),
]
