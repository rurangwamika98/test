from django.urls import path
from .views import generate_manifest, manifests, sign_receipt, verify_license

urlpatterns = [
    path("manifests/", manifests),
    path("ebm/sign-receipt/", sign_receipt),
    path("rura/verify-license/<str:license_no>/", verify_license),
    path("customs/generate-manifest/", generate_manifest),
]
