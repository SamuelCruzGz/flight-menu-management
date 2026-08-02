from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Dish(Base):
    __tablename__ = "dishes"

    id: Mapped[int] = mapped_column(primary_key=True)

    menu_id: Mapped[int] = mapped_column(
        ForeignKey("menus.id"),
        nullable=False,
    )

    meal_code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    name_es: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    name_en: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description_es: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    description_en: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    image_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    availability: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,        
    )
    