from pydantic import BaseModel
from app.schemas.common import AirportCode, FlightNumber


class FlightValidationRequest(BaseModel):
    flight_number: FlightNumber
    departure_airport: AirportCode
    arrival_airport: AirportCode
    
    
class FlightValidationResponse(BaseModel):
    exists: bool
    flight_id: int | None