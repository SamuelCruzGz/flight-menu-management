from datetime import date

from sqlalchemy.orm import Session

from app.core.validation import validate_duplicate_dishes
from app.exceptions.menu import FlightNotFoundException
from app.models.flight import Flight
from app.core.normalization import normalize_menu_cycle
from app.models.menu import Menu
from app.repositories.flight import FlightRepository
from app.repositories.menu import MenuRepository
from app.models.dish import Dish
from app.schemas.common import (
    FlightNumber,
    MenuCycle,
    MenuStatus,
)
from app.schemas.menu import (
    MenuCreateRequest,
    MenuResponse,
)


class MenuService:

    def __init__(
        self,
        menu_repository: MenuRepository,
        flight_repository: FlightRepository,
        db: Session,
    ):
        self.menu_repository = menu_repository
        self.flight_repository = flight_repository
        self.db = db

    def create(
        self,
        request: MenuCreateRequest,
    ) -> MenuResponse:

        cycle = self._normalize_cycle(
            request.cycle,
        )

        status = self._calculate_status(
            request.start_date,
            request.end_date,
        )

        flight = self._resolve_flight(
            request.flight_number,
        )

        validate_duplicate_dishes(
            request.dishes,
        )

        menu = self._create_menu(
            request=request,
            flight=flight,
            cycle=cycle,
            status=status,
        )

        try:
            menu = self.menu_repository.create(menu)

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise

        return self._build_response(menu)

    def _resolve_flight(
        self,
        flight_number: FlightNumber,
    ) -> Flight:
        """
        Resolve a flight using its business identifier.

        Raises:
            FlightNotFoundException:
                If the flight does not exist.
        """

        flight = self.flight_repository.get_by_flight_number(
            flight_number,
        )

        if flight is None:
            raise FlightNotFoundException()

        return flight

    def _calculate_status(
        self,
        start_date: date,
        end_date: date,
    ) -> MenuStatus:
        """
        Calculate the menu status based on the current date.
        """

        if date.today() > end_date:
            return MenuStatus.INACTIVE

        return MenuStatus.ACTIVE

    def _normalize_cycle(
        self,
        cycle: MenuCycle,
    ) -> MenuCycle:
        """
        Normalize the menu cycle into its canonical representation.
        """

        return normalize_menu_cycle(cycle)

    def _create_menu(
        self,
        request: MenuCreateRequest,
        flight: Flight,
        cycle: MenuCycle,
        status: MenuStatus,
    ) -> Menu:
        """
        Build a Menu aggregate from the validated request.
        """

        menu = Menu(
            flight_id=flight.id,
            start_date=request.start_date,
            end_date=request.end_date,
            cycle=cycle,
            status=status,
            created_by="system",  # TODO: Replace with authenticated user.
        )

        menu.dishes = [
            Dish(
                meal_code=dish.meal_code,
                name_es=dish.name_es,
                name_en=dish.name_en,
                description_es=dish.description_es,
                description_en=dish.description_en,
                image_url=str(dish.image_url),
                availability=dish.availability,
            )
            for dish in request.dishes
        ]

        return menu
        
    def _build_response(
        self,
        menu: Menu,
    ) -> MenuResponse:
        """
        Convert a persisted Menu ORM model into an API response.
        """

        return MenuResponse(
            id=menu.id,
            flight_number=menu.flight.flight_number,
            start_date=menu.start_date,
            end_date=menu.end_date,
            cycle=menu.cycle,
            status=menu.status,
            created_by=menu.created_by,
            created_at=menu.created_at,
            deleted_at=menu.deleted_at,
        )