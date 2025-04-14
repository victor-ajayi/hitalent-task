from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ReservationBase(BaseModel):
    model_config = ConfigDict(extra="ignore")

    customer_name: str
    phone_number: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int


class ReservationCreate(ReservationBase):
    pass


class Reservation(ReservationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime | None
