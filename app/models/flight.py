from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Flight(Base):
    __tablename__ = "flights"

    id: Mapped[int] = mapped_column(primary_key=True)

    flight_number: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    departure_airport: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )

    arrival_airport: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )

    carrier: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )