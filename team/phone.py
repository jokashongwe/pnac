import re


def normalize_phone(value):
    """Return an international digit-only number (e.g. 2438...) or empty string."""
    if not value:
        return ""
    digits = re.sub(r"\D", "", str(value))
    if digits.startswith("00"):
        digits = digits[2:]
    if digits.startswith("0") and len(digits) in (9, 10):
        digits = "243" + digits.lstrip("0")
    elif len(digits) == 9 and digits[0] in "89":
        digits = "243" + digits
    return digits
