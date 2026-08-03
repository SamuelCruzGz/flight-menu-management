from dataclasses import dataclass
from datetime import date

from app.schemas.common import (
    FlightNumber,
    MenuStatus,
)


@dataclass(slots=True)
class MenuFilter:

    flight_number: FlightNumber | None = None

    start_date: date | None = None

    end_date: date | None = None

    status: MenuStatus | None = None

    page_number: int = 1

    page_size: int = 20