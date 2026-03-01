from django.urls import path

from core.views import RegisterView, verify_nid_view
from .views import IshemaTokenObtainView, IshemaTokenRefreshView, session_login, universal_logout, whoami

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("verify-nid/", verify_nid_view),
    path("login/session/", session_login),
    path("logout/", universal_logout),
    path("token/obtain/", IshemaTokenObtainView.as_view()),
    path("token/refresh/", IshemaTokenRefreshView.as_view()),
    path("whoami/", whoami),
]
