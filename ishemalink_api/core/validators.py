import re

PHONE_REGEX = re.compile(r"^\+2507\d{8}$")
NID_REGEX = re.compile(r"^1\d{15}$")


def validate_rwanda_phone(phone: str) -> bool:
    return bool(PHONE_REGEX.fullmatch(phone))


def validate_nid(nid: str) -> bool:
    return bool(NID_REGEX.fullmatch(nid))
