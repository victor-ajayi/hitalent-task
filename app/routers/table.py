from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import schemas
from app.core.database import get_db
from app.services import table as services

router = APIRouter(prefix="/tables", tags=["Table"])


@router.get("/")
def get_tables(session: Annotated[Session, Depends(get_db)]) -> list[schemas.Table]:
    return services.get_all_tables(session)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_table(
    session: Annotated[Session, Depends(get_db)], table_create: schemas.TableCreate
) -> schemas.Table:
    try:
        table = services.create_table(session, table_create)
    except Exception as e:
        raise HTTPException(
            detail=f"An error occured while creating table: {str(e)}", status_code=400
        )

    return table


@router.delete("/{table_id}")
def delete_table(session: Annotated[Session, Depends(get_db)], table_id: int):
    try:
        services.delete_table(session, table_id)
    except Exception as e:
        raise HTTPException(
            detail=f"An error occured while deleting table: {str(e)}", status_code=400
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
