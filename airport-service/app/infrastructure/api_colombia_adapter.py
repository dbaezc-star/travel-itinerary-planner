import logging
from typing import List, Optional
import httpx
from app.domain.models import Airport
from app.domain.ports import AirportPort

logger = logging.getLogger(__name__)
API_BASE = "https://api-colombia.com/api/v1"

class APIColombiaAdapter(AirportPort):
    """Adapter que traduce la API Colombia al modelo de dominio interno."""

    def __init__(self, timeout: float = 10.0):
        self._timeout = timeout

    def _fetch(self, path: str):
        """Hace la petición HTTP a la API Colombia."""
        response = httpx.get(f"{API_BASE}{path}", timeout=self._timeout)
        response.raise_for_status()
        return response.json()

    def _translate(self, raw: dict) -> Optional[Airport]:
        """Traduce el objeto externo al modelo Airport del dominio."""
        try:
            city = raw.get("city", {})
            city_name = city.get("name", "") if isinstance(city, dict) else str(city)
            dept = city.get("departmentName", "") if isinstance(city, dict) else ""
            return Airport(
                id=int(raw["id"]),
                name=raw.get("name") or "",
                city=city_name,
                department=dept,
                latitude=float(raw.get("latitude") or 0),
                longitude=float(raw.get("longitude") or 0),
                iata_code=raw.get("iataCode"),
            )
        except (KeyError, TypeError, ValueError) as e:
            logger.warning("No se pudo traducir aeropuerto %s: %s", raw.get("id"), e)
            return None

    def get_all(self) -> List[Airport]:
        """Obtiene todos los aeropuertos colombianos."""
        try:
            data = self._fetch("/Airport")
            if isinstance(data, dict):
                data = data.get("data", [])
            return [a for item in data if (a := self._translate(item)) is not None]
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"API Colombia error {e.response.status_code}") from e
        except httpx.RequestError as e:
            raise RuntimeError("No se pudo conectar a API Colombia") from e

    def get_by_id(self, airport_id: int) -> Optional[Airport]:
        """Obtiene un aeropuerto por su ID."""
        try:
            data = self._fetch(f"/Airport/{airport_id}")
            if isinstance(data, list):
                data = data[0] if data else None
            return self._translate(data) if data else None
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise RuntimeError(f"API Colombia error {e.response.status_code}") from e
        except httpx.RequestError as e:
            raise RuntimeError("No se pudo conectar a API Colombia") from e