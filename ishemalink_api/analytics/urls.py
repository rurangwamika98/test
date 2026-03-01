from django.urls import path
from .views import commodity_breakdown, drivers_leaderboard, revenue_heatmap, routes_top

urlpatterns = [
    path("routes/top/", routes_top),
    path("commodities/breakdown/", commodity_breakdown),
    path("revenue/heatmap/", revenue_heatmap),
    path("drivers/leaderboard/", drivers_leaderboard),
]
