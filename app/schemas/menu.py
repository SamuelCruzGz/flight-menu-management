from datetime import date, datetime

from pydantic import BaseModel, Field, model_validator

from app.schemas.common import (
    FlightNumber,
    MenuCycle,
    MenuStatus,
    UserName,
)
from app.schemas.dish import (
    DishCreateRequest,
    DishResponse,
)


class MenuBase(BaseModel):
    start_date: date

    end_date: date

    cycle: MenuCycle

    @model_validator(mode="after")
    def validate_date_range(self):
        if self.end_date < self.start_date:
            raise ValueError(
                "end_date must be greater than or equal to start_date."
            )

        return self


class MenuCreateRequest(MenuBase):
    flight_number: FlightNumber

    dishes: list[DishCreateRequest] = Field(
        min_length=1,
    )


class MenuUpdateRequest(MenuBase):
    dishes: list[DishCreateRequest] = Field(
        min_length=1,
    )

class MenuSearchRequest(BaseModel):

    flight_number: FlightNumber | None = None

    start_date: date | None = None

    end_date: date | None = None

    status: MenuStatus | None = None

    page_number: int = 1

    page_size: int = 20


class MenuResponse(BaseModel):
    id: int

    flight_number: FlightNumber

    start_date: date

    end_date: date

    cycle: MenuCycle

    status: MenuStatus

    created_by: UserName

    created_at: datetime

    deleted_at: datetime | None


class MenuDetailResponse(MenuResponse):
    dishes: list[DishResponse]


class PaginatedMenuResponse(BaseModel):
    items: list[MenuResponse]

    total_records: int

    total_pages: int

    page_number: int

    page_size: int