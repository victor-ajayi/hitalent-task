from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.table import Table


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_name: Mapped[str]
    phone_number: Mapped[str]
    reservation_time: Mapped[datetime]
    duration_minutes: Mapped[int]

    table: Mapped["Table"] = relationship(back_populates="reservations")
    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id", ondelete="CASCADE"))

    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.current_timestamp()
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=True, onupdate=func.current_timestamp()
    )
