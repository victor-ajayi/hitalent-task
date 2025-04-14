from fastapi import APIRouter

from app.routers import reservation, table

api_router = APIRouter()

api_router.include_router(table.router)
api_router.include_router(reservation.router)


@api_router.get("/ping")
def health_check():
    return {"status": "Healthy!"}
