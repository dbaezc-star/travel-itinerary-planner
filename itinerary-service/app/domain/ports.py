from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models import Itinerary

class ItineraryRepository(ABC):
    """Puerto de dominio — contrato para persistencia de itinerarios."""

    @abstractmethod
    def save(self, itinerary: Itinerary) -> Itinerary:
        """Guarda un nuevo itinerario."""
        ...

    @abstractmethod
    def find_all(self) -> List[Itinerary]:
        """Retorna todos los itinerarios."""
        ...

    @abstractmethod
    def find_by_id(self, itinerary_id: int) -> Optional[Itinerary]:
        """Retorna un itinerario por su ID."""
        ...

    @abstractmethod
    def update(self, itinerary: Itinerary) -> Itinerary:
        """Actualiza un itinerario existente."""
        ...

    @abstractmethod
    def delete(self, itinerary_id: int) -> bool:
        """Elimina un itinerario por su ID."""
        ...

class AirportValidationPort(ABC):
    """Puerto de dominio — contrato para validar aeropuertos."""

    @abstractmethod
    def airport_exists(self, airport_id: int) -> bool:
        """Verifica si un aeropuerto existe en el Airport Service."""
        ...
        