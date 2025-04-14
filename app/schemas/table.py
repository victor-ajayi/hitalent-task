from pydantic import BaseModel, ConfigDict

from app.models.table import TableLocations


class TableBase(BaseModel):
    model_config = ConfigDict(extra="ignore", use_enum_values=True)

    name: str
    seats: int
    location: TableLocations


class TableCreate(TableBase):
    pass


class Table(TableBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
