from django.urls import path

from .views import AgentOnboardView, MeView

urlpatterns = [
    path("me/", MeView.as_view()),
    path("agents/onboard/", AgentOnboardView.as_view()),
]
