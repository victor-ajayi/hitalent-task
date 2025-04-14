from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.core.database import get_db
from app.main import app
from app.models import Base
from app.models.reservation import Reservation
from app.models.table import Table

engine = create_engine(settings.get_database_url)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_tables(session: Session):
    tables = [
        {"name": "Table 1", "seats": 2, "location": "HALL_CENTRE"},
        {"name": "Table 2", "seats": 4, "location": "TERRACE"},
    ]
    tables = session.scalars(insert(Table).returning(Table), tables)
    return tables


@pytest.fixture
def test_reservations(session: Session, test_tables):
    reservations = [
        {
            "customer_name": "Ivan",
            "phone_number": "+79001234567",
            "table_id": 1,
            "reservation_time": datetime.fromisoformat("2025-04-15 12:00:00"),
            "duration_minutes": 120,
        },
        {
            "customer_name": "Elena",
            "phone_number": "+79001239876",
            "table_id": 2,
            "reservation_time": datetime.fromisoformat("2025-04-15 13:00:00"),
            "duration_minutes": 120,
        },
    ]

    reservations = session.scalars(
        insert(Reservation).returning(Reservation), reservations
    ).all()

    return reservations
