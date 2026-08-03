from sqlalchemy import select
from sqlalchemy.orm import Session

from app.filters.menu import MenuFilter
from app.models.flight import Flight
from app.models.menu import Menu
from datetime import date

class MenuRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        menu: Menu,
    ) -> Menu:

        self.db.add(menu)

        self.db.flush()

        self.db.refresh(menu)

        return menu

    def get_by_id(
        self,
        menu_id: int,
    ) -> Menu | None:

        statement = (
            select(Menu)
            .where(
                Menu.id == menu_id,
                Menu.deleted_at.is_(None),
            )
        )

        result = self.db.execute(statement)

        return result.scalar_one_or_none()

    def update(
        self,
        menu: Menu,
    ) -> Menu:

        self.db.flush()

        self.db.refresh(menu)

        return menu

    def soft_delete(
        self,
        menu: Menu,
    ) -> None:

        self.db.flush()

    def search(
        self,
        filters: MenuFilter,
    ) -> list[Menu]:

        statement = (
            select(Menu)
            .join(Menu.flight)
            .where(
                Menu.deleted_at.is_(None),
            )
        )

        if filters.flight_number is not None:
            statement = statement.where(
                Flight.flight_number == filters.flight_number,
            )

        if filters.start_date is not None:
            statement = statement.where(
                Menu.start_date >= filters.start_date,
            )

        if filters.end_date is not None:
            statement = statement.where(
                Menu.end_date <= filters.end_date,
            )

        if filters.status is not None:
            statement = statement.where(
                Menu.status == filters.status,
            )

        statement = statement.order_by(
            Menu.created_at.desc(),
        )

        offset = (
            filters.page_number - 1
        ) * filters.page_size

        statement = (
            statement
            .offset(offset)
            .limit(filters.page_size)
        )

        result = self.db.execute(statement)

        return result.scalars().all()
    
    
    def exists(
        self,
        flight_id: int,
        start_date: date,
        end_date: date,
    ) -> bool:
        statement = (
        select(Menu.id)
            .where(
                Menu.flight_id == flight_id,
                Menu.start_date == start_date,
                Menu.end_date == end_date,
                Menu.deleted_at.is_(None),
            )
        )

        result = self.db.execute(statement)

        return result.scalar_one_or_none() is not None