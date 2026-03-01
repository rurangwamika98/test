from django.urls import path
from .views import anonymize, consent_history, my_data

urlpatterns = [
    path("my-data/", my_data),
    path("anonymize/", anonymize),
    path("consent-history/", consent_history),
]
