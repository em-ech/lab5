from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Optional


class BikeBase(BaseModel):
    model: str
    battery_level: float = Field(le=100)
    status: Literal["available", "rented", "maintenance"]
    station_id: Optional[int] = None


class BikeCreate(BikeBase):
    pass


class BikeResponse(BikeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
