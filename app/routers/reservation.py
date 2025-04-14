from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import schemas
from app.core.database import get_db
from app.services import reservation as services

router = APIRouter(prefix="/reservations", tags=["Reservation"])


@router.get("/")
def get_reservations(
    session: Annotated[Session, Depends(get_db)],
) -> list[schemas.Reservation]:
    return services.get_reservations(session)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_reservation(
    session: Annotated[Session, Depends(get_db)],
    reservation_create: schemas.ReservationCreate,
) -> schemas.Reservation:
    try:
        return services.create_reservation(session, reservation_create)
    except Exception as e:
        raise HTTPException(detail=f"{str(e)}", status_code=status.HTTP_400_BAD_REQUEST)


@router.delete("/{reservation_id}")
def delete_reservation(
    session: Annotated[Session, Depends(get_db)], reservation_id: int
):
    try:
        services.delete_reservation(session, reservation_id)
    except Exception:
        raise HTTPException(
            detail="An error occured while deleting reservation",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
