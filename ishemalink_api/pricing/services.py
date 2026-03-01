from decimal import Decimal
from django.core.cache import cache

from .models import Tariff


class PriceCalculator:
    cache_key = "tariff_rates_v1"

    def get_rates(self):
        rates = cache.get(self.cache_key)
        if rates:
            return rates, True
        rates = {t.zone: {"base": t.base_price, "kg_rate": t.kg_rate} for t in Tariff.objects.all()}
        if not rates:
            rates = {
                "ZONE_1": {"base": 1500, "kg_rate": 100},
                "ZONE_2": {"base": 2500, "kg_rate": 200},
                "ZONE_3": {"base": 4500, "kg_rate": 350},
            }
        cache.set(self.cache_key, rates, timeout=600)
        return rates, False

    def calculate(self, weight_kg: Decimal, destination: str) -> Decimal:
        rates, _ = self.get_rates()
        zone = "ZONE_1" if "Kigali" in destination else "ZONE_2"
        if destination in {"Kampala", "Nairobi", "Goma"}:
            zone = "ZONE_3"
        cfg = rates.get(zone, rates["ZONE_2"])
        return Decimal(cfg["base"]) + (Decimal(cfg["kg_rate"]) * Decimal(weight_kg))
