from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app import schemas
from app.models.table import Table


def get_table(session: Session, table_id: int):
    return session.scalar(select(Table).where(Table.id == table_id))


def get_all_tables(session: Session):
    return session.scalars(select(Table)).all()


def create_table(
    session: Session,
    table_create: schemas.TableCreate,
):
    table = Table(**table_create.model_dump())
    session.add(table)
    session.commit()
    session.refresh(table)

    return table


def delete_table(session: Session, table_id: int):
    session.execute(delete(Table).where(Table.id == table_id))
    session.commit()
