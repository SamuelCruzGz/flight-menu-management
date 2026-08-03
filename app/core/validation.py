from app.core.normalization import normalize_dish_name
from app.schemas.dish import DishCreateRequest


def validate_duplicate_dishes(
    dishes: list[DishCreateRequest],
) -> None:

    seen: set[tuple[str, str]] = set()

    for dish in dishes:

        key = (
            normalize_dish_name(dish.name_es),
            normalize_dish_name(dish.name_en),
        )

        if key in seen:
            raise ValueError(
                "Duplicated dishes are not allowed."
            )

        seen.add(key)