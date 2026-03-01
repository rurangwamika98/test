from ishemalink_api.core.validators import validate_nid, validate_rwanda_phone


def test_validate_rwanda_phone_accepts_valid_number() -> None:
    assert validate_rwanda_phone("+250788123456") is True


def test_validate_rwanda_phone_rejects_invalid_number() -> None:
    assert validate_rwanda_phone("0788123456") is False


def test_validate_nid_accepts_valid_format() -> None:
    assert validate_nid("1234567890123456") is True


def test_validate_nid_rejects_invalid_format() -> None:
    assert validate_nid("023456789012345") is False
