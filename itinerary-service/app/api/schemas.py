from pydantic import BaseModel, Field, model_validator
from datetime import date
from typing import Optional

class ItineraryCreate(BaseModel):
    user_name: str = Field(..., min_length=1, max_length=100)
    departure_airport_id: int = Field(..., gt=0)
    arrival_airport_id: int = Field(..., gt=0)
    travel_date: date
    duration_minutes: int = Field(..., gt=0)

    @model_validator(mode='after')
    def airports_different(self):
        if self.departure_airport_id == self.arrival_airport_id:
            raise ValueError('El aeropuerto de salida y llegada deben ser diferentes')
        return self

class ItineraryUpdate(BaseModel):
    user_name: Optional[str] = Field(None, min_length=1, max_length=100)
    departure_airport_id: Optional[int] = Field(None, gt=0)
    arrival_airport_id: Optional[int] = Field(None, gt=0)
    travel_date: Optional[date] = None
    duration_minutes: Optional[int] = Field(None, gt=0)

class ItineraryResponse(BaseModel):
    id: int
    user_name: str
    departure_airport_id: int
    arrival_airport_id: int
    travel_date: date
    duration_minutes: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
