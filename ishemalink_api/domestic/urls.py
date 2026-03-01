from django.urls import path
from .views import ShipmentListView, batch_update, create_shipment, live_tracking, tracking_history, update_status

urlpatterns = [
    path("", ShipmentListView.as_view()),
    path("create/", create_shipment),
    path("batch-update/", batch_update),
    path("<int:pk>/update-status/", update_status),
    path("<int:pk>/tracking/", tracking_history),
    path("tracking/<str:tracking_code>/live/", live_tracking),
]
