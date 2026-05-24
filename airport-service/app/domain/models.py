from dataclasses import dataclass
from typing import Optional

@dataclass
class Airport:
    id: int
    name: str
    city: str
    department: str
    latitude: float
    longitude: float
    iata_code: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "department": self.department,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "iata_code": self.iata_code,
        }