from datetime import date, datetime
from sqlalchemy import ForeignKey, String, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Menu(Base):
    
    __table_args__ = (
        UniqueConstraint(
            "flight_id",
            "start_date",
            "end_date",
            name="uq_menu_flight_dates",
        ),
    )
    __tablename__ = "menus"

    id: Mapped[int] = mapped_column(primary_key=True)

    flight_id: Mapped[int] = mapped_column(
        ForeignKey("flights.id"),
        nullable=False,
    )

    start_date: Mapped[date] = mapped_column(nullable=False)

    end_date: Mapped[date] = mapped_column(nullable=False)

    cycle: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    created_by: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )