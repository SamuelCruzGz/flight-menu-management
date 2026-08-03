from enum import StrEnum
from typing import Annotated

from pydantic import Field, HttpUrl


AirportCode = Annotated[
    str,
    Field(
        min_length=3,
        max_length=3,
    ),
]

FlightNumber = Annotated[
    str,
    Field(
        min_length=1,
        max_length=10,
    ),
]

LocalizedName = Annotated[
    str,
    Field(
        min_length=1,
        max_length=100,
    ),
]

LocalizedDescription = Annotated[
    str,
    Field(
        min_length=1,
    ),
]

ImageUrl = HttpUrl

MenuCycle = Annotated[
    str,
    Field(
        pattern=r"^(?i)(week|semana)_[0-9]+$",
    ),
]

UserName = Annotated[
    str,
    Field(
        min_length=1,
        max_length=100,
    ),
]


class MenuStatus(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class MealCode(StrEnum):
    BREAKFAST = "BREAKFAST"
    LUNCH = "LUNCH"
    DINNER = "DINNER"