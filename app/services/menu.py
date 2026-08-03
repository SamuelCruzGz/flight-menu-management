from __future__ import annotations

from datetime import date

from sqlalchemy.orm import Session

from app.core.validation import validate_duplicate_dishes
from app.exceptions.menu import (
    FlightNotFoundException,
    MenuNotFoundException,
    DuplicateMenuException,
)
from app.models.flight import Flight
from app.core.normalization import normalize_menu_cycle
from app.models.menu import Menu
from app.repositories.flight import FlightRepository
from app.repositories.menu import MenuRepository
from app.models.dish import Dish
from app.filters.menu import MenuFilter
from app.schemas.dish import DishCreateRequest
from app.schemas.common import (
    FlightNumber,
    MenuCycle,
    MenuStatus,
)
from app.schemas.menu import (
    MenuCreateRequest,
    MenuUpdateRequest,
    MenuSearchRequest,
    MenuResponse,
    PaginatedMenuResponse,
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
        """
        Create a menu and its associated dishes.
        """

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
        
        self._validate_duplicate_menu(
            flight.id,
            request.start_date,
            request.end_date,
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
    
    
    def get(
        self,
        menu_id: int,
    ) -> MenuResponse:
        """
        Retrieve a menu by its identifier.
        """

        menu = self._resolve_menu(menu_id)

        return self._build_response(menu)                    
    
    
                
    def list(
        self,
        page_number: int,
        page_size: int,
    ) -> PaginatedMenuResponse:
        """
        Retrieve a paginated list of menus.
        """

        return self.search(
            MenuSearchRequest(
                page_number=page_number,
                page_size=page_size,
            )
        )
        
    
    def search(
        self,
        request: MenuSearchRequest,
        ) -> PaginatedMenuResponse:
        """
        Search menus using the provided filters.
        """

        filters = MenuFilter(
            flight_number=request.flight_number,
            start_date=request.start_date,
            end_date=request.end_date,
            status=request.status,
            page_number=request.page_number,
            page_size=request.page_size,
        )

        return self._search(
            filters,
        )
        
    
    def delete(
        self,
        menu_id: int,
    ) -> None:
        """
        Logically delete a menu.
        """

        menu = self._resolve_menu(menu_id)

        try:
            self.menu_repository.soft_delete(
                menu,
            )

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise


    def update(
        self,
        menu_id: int,
        request: MenuUpdateRequest,
    ) -> MenuResponse:
        """
        Update an existing menu.
        """

        menu = self._resolve_menu(
            menu_id,
        )

        validate_duplicate_dishes(
            request.dishes,
        )

        cycle = self._normalize_cycle(
            request.cycle,
        )

        status = self._calculate_status(
            request.start_date,
            request.end_date,
        )

        self._validate_duplicate_menu(
            flight_id=menu.flight_id,
            start_date=request.start_date,
            end_date=request.end_date,
            exclude_menu_id=menu.id,
        )

        menu.start_date = request.start_date
        menu.end_date = request.end_date
        menu.cycle = cycle
        menu.status = status

        self._replace_dishes(
            menu,
            request.dishes,
        )

        try:
            menu = self.menu_repository.update(
                menu,
            )

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise

        return self._build_response(
            menu,
        )


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
    
    
    def _resolve_menu(
        self,
        menu_id: int,
    ) -> Menu:
        """
        Resolve a menu by its identifier.
        """

        menu = self.menu_repository.get_by_id(
            menu_id,
        )

        if menu is None:
            raise MenuNotFoundException()

        return menu
    

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
    
    
    def _search(
        self,
        filters: MenuFilter,
        ) -> PaginatedMenuResponse:
        """
        Execute a paginated menu search.
        """

        menus = self.menu_repository.search(
            filters,
        )

        total_records = self.menu_repository.count(
            filters,
        )

        total_pages = (
            total_records + filters.page_size - 1
        ) // filters.page_size

        return PaginatedMenuResponse(
            items=[
                self._build_response(menu)
                for menu in menus
            ],
            total_records=total_records,
            total_pages=total_pages,
            page_number=filters.page_number,
            page_size=filters.page_size,
        )


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
            created_by="system",  
        )

        menu.dishes = self._build_dishes(
            request.dishes,
        )
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
        
    
    def _validate_duplicate_menu(
        self,
        flight_id: int,
        start_date: date,
        end_date: date,
        exclude_menu_id: int | None = None,
    ) -> None:
        """
        Ensure there is no duplicated menu for the same
        flight and date range.
        """

        if self.menu_repository.exists(
            flight_id=flight_id,
            start_date=start_date,
            end_date=end_date,
            exclude_menu_id=exclude_menu_id,
        ):
            raise DuplicateMenuException()
    

    def _build_dishes(
        self,
        dishes: list[DishCreateRequest],
    ) -> list[Dish]:
        """
        Build Dish entities from the request.
        """

        return [
            Dish(
                meal_code=dish.meal_code,
                name_es=dish.name_es,
                name_en=dish.name_en,
                description_es=dish.description_es,
                description_en=dish.description_en,
                image_url=str(dish.image_url),
                availability=dish.availability,
            )
            for dish in dishes
        ]
        
        
    def _replace_dishes(
        self,
        menu: Menu,
        dishes: list[DishCreateRequest],
    ) -> None:
        """
        Replace all dishes associated with a menu.
        """

        menu.dishes.clear()

        menu.dishes.extend(
            self._build_dishes(
                dishes,
            )
        )