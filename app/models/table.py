import enum

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.reservation import Reservation


class TableLocations(enum.Enum):
    HALL_CENTRE = "HALL_CENTRE"
    HALL_WALL = "HALL_WALL"
    HALL_WINDOW = "HALL_WINDOW"
    TERRACE = "TERRACE"


class Table(Base):
    __tablename__ = "tables"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=50))
    seats: Mapped[int]
    location: Mapped[str]

    reservations: Mapped[list["Reservation"]] = relationship(back_populates="table")
