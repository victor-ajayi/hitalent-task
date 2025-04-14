from datetime import timedelta

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app import schemas
from app.models.reservation import Reservation
from app.models.table import Table


def get_reservation(session: Session, reservation_id: int) -> Reservation | None:
    return session.scalar(select(Reservation).where(Reservation.id == reservation_id))


def get_reservations(session: Session):
    return session.scalars(select(Reservation)).all()


def create_reservation(session: Session, reservation_create: schemas.ReservationCreate):
    table = session.scalar(select(Table).where(Table.id == reservation_create.table_id))

    if not table:
        raise Exception("Table does not exist.")

    def is_table_available(new_start, new_end):
        reservations = (
            session.execute(
                select(Reservation).where(
                    Reservation.table_id == reservation_create.table_id
                )
            )
            .scalars()
            .all()
        )

        for r in reservations:
            r_end = r.reservation_time + timedelta(minutes=r.duration_minutes)
            if r.reservation_time < new_end and r_end > new_start:
                return False
        return True

    new_start = reservation_create.reservation_time
    new_end = new_start + timedelta(minutes=reservation_create.duration_minutes)

    if not is_table_available(new_start, new_end):
        raise Exception("Table not available for reservation at provided time.")

    reservation = Reservation(**reservation_create.model_dump())
    session.add(reservation)
    session.commit()
    session.refresh(reservation)

    return reservation


def delete_reservation(session: Session, reservation_id: int):
    session.execute(delete(Reservation).where(Reservation.id == reservation_id))
    session.commit()
