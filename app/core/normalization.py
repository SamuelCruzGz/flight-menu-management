import re

from app.schemas.common import MenuCycle


def normalize_dish_name(
    name: str,
) -> str:
    """
    Normalize a dish name for comparison purposes.

    The normalized value is used only during validation
    and is never persisted.
    """

    normalized = name.strip()

    normalized = normalized.upper()

    normalized = re.sub(
        r"\s+",
        " ",
        normalized,
    )

    return normalized


def normalize_menu_cycle(
    cycle: MenuCycle,
) -> MenuCycle:
    """
    Normalize a menu cycle into its canonical representation.

    Examples:
        week_1    -> week_1
        Week_1    -> week_1
        semana_1  -> week_1
    """

    normalized = cycle.strip().lower()

    normalized = normalized.replace(
        "semana_",
        "week_",
    )

    return normalized