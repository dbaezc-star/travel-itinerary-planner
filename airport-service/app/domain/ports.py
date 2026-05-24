from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models import Airport

class AirportPort(ABC):
    """Puerto de dominio — define el contrato para obtener aeropuertos."""

    @abstractmethod
    def get_all(self) -> List[Airport]:
        """Retorna todos los aeropuertos disponibles."""
        ...

    @abstractmethod
    def get_by_id(self, airport_id: int) -> Optional[Airport]:
        """Retorna un aeropuerto por su ID, o None si no existe."""
        ...