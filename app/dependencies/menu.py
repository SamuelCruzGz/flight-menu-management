from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.flight import FlightRepository
from app.repositories.menu import MenuRepository
from app.services.menu import MenuService


def get_menu_service(
    db: Session = Depends(get_db),
) -> MenuService:
    """
    Build the MenuService with its dependencies.
    """

    menu_repository = MenuRepository(
        db,
    )

    flight_repository = FlightRepository(
        db,
    )

    return MenuService(
        menu_repository=menu_repository,
        flight_repository=flight_repository,
        db=db,
    )