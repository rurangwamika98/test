from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.cache import cache

from .services import PriceCalculator


@api_view(["GET"])
def tariffs_view(request):
    calc = PriceCalculator()
    rates, cache_hit = calc.get_rates()
    response = Response({"cached_at": "dynamic", "rates": rates})
    response["X-Cache-Hit"] = "TRUE" if cache_hit else "FALSE"
    response["Cache-Control"] = "public, max-age=300"
    return response


@api_view(["POST"])
def calculate_view(request):
    weight = request.data.get("weight_kg", 1)
    destination = request.data.get("destination", "Kigali")
    price = PriceCalculator().calculate(weight, destination)
    return Response({"price_rwf": str(price)})


@api_view(["POST"])
def clear_tariffs_cache(request):
    cache.delete(PriceCalculator.cache_key)
    return Response({"message": "Tariff cache cleared"})
