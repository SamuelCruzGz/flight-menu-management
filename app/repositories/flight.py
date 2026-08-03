from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.flight import Flight
from app.schemas.common import AirportCode, FlightNumber


class FlightRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_route(
        self,
        flight_number: FlightNumber,
        departure_airport: AirportCode,
        arrival_airport: AirportCode,
    ) -> Flight | None:

        statement = (
            select(Flight)
            .where(
                Flight.flight_number == flight_number,
                Flight.departure_airport == departure_airport,
                Flight.arrival_airport == arrival_airport,
            )
        )

        return (
            self.db.execute(statement)
            .scalar_one_or_none()
        )