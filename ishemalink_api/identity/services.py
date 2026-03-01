import random
from django.core.cache import cache


def generate_otp(phone: str) -> str:
    code = f"{random.randint(0, 999999):06d}"
    cache.set(f"otp:{phone}", code, timeout=300)
    return code


def verify_otp(phone: str, code: str) -> bool:
    cached = cache.get(f"otp:{phone}")
    if cached and cached == code:
        cache.delete(f"otp:{phone}")
        return True
    return False
