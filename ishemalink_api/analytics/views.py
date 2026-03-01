from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def routes_top(request):
    return Response({"routes": []})


@api_view(["GET"])
def commodity_breakdown(request):
    return Response({"commodities": []})


@api_view(["GET"])
def revenue_heatmap(request):
    return Response({"sectors": []})


@api_view(["GET"])
def drivers_leaderboard(request):
    return Response({"drivers": []})
