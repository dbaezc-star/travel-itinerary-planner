from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

@dataclass
class Itinerary:
    user_name: str
    departure_airport_id: int
    arrival_airport_id: int
    travel_date: date
    duration_minutes: int
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_name': self.user_name,
            'departure_airport_id': self.departure_airport_id,
            'arrival_airport_id': self.arrival_airport_id,
            'travel_date': self.travel_date.isoformat() if self.travel_date else None,
            'duration_minutes': self.duration_minutes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
