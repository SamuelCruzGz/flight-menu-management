from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.flight import FlightRepository
from app.services.flight import FlightService


def get_flight_service(
    db: Session = Depends(get_db),
) -> FlightService:
    """
    Build the FlightService with its dependencies.
    """

    repository = FlightRepository(
        db,
    )

    return FlightService(
        repository,
    )