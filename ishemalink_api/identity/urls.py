from django.urls import path
from .views import identity_register, identity_status, kyc_nid, verify_otp_view

urlpatterns = [
    path("register/", identity_register),
    path("verify-otp/", verify_otp_view),
    path("kyc/nid/", kyc_nid),
    path("status/", identity_status),
]
