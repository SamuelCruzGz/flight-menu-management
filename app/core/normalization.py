import re


def normalize_dish_name(name: str) -> str:
    """
    Normalize a dish name for comparison purposes.

    The normalized value is used only during validation
    and is never persisted.
    """

    normalized = name.strip()

    normalized = normalized.upper()

    normalized = re.sub(r"\s+", " ", normalized)

    return normalized