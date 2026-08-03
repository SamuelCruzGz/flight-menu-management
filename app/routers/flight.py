from fastapi import APIRouter, Depends

from app.dependencies.flight import get_flight_service
from app.schemas.flight import (
    FlightValidationRequest,
    FlightValidationResponse,
)
from app.services.flight import FlightService


router = APIRouter(
    prefix="/api/v1/flights",
    tags=["Flights"],
)


@router.post(
    "/validate",
    response_model=FlightValidationResponse,
)
def validate_flight(
    request: FlightValidationRequest,
    service: FlightService = Depends(get_flight_service),
) -> FlightValidationResponse:

    return service.validate(request)