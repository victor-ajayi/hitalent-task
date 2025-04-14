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
        # Вероятно, мы могли бы написать более эффективную логику на уровне базы данных таким образом:

        # session.execute(
        #     select(Reservation)
        #     .where(
        #         Reservation.table_id == table_id,
        #         Reservation.reservation_time < new_end,
        #         (
        #             Reservation.reservation_time
        #             + func.make_interval(
        #                 mins=cast(Reservation.duration_minutes, Integer)
        #             )
        #         )
        #         > new_start,
        #     )
        #     .limit(1)
        # ).first()

        # Но здесь нужно помнить один нуанс – функция func.make_interval специфична для PostgreSQL. Мы бы написали логику для конкретной базы данных, чтобы вычислить `reservation_time + timedelta` для каждой строки. Предположим, мы меняем нашу базу данных на SQLite или что-то еще, наш код сразу же ломается. Поэтому для простоты мы вычисляем это в памяти. Поскольку наш вариант использования - ресторан, сохраненные данные в таблице бронирования объективно не превышают нескольких сотен строк.

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
