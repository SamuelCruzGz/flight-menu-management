from app.repositories.flight import FlightRepository
from app.schemas.flight import (
    FlightValidationRequest,
    FlightValidationResponse,
)

class FlightService:

    def __init__(
        self,
        repository: FlightRepository,
    ):
        self.repository = repository

    def validate(
        self,
        request: FlightValidationRequest,
    ) -> FlightValidationResponse:

        flight = self.repository.get_by_route(
            flight_number=request.flight_number,
            departure_airport=request.departure_airport,
            arrival_airport=request.arrival_airport,
        )

        return FlightValidationResponse(
            exists=flight is not None,
            flight_id=flight.id if flight else None,
        )