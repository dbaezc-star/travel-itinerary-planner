import os
import logging
import httpx
from app.domain.ports import AirportValidationPort

logger = logging.getLogger(__name__)
AIRPORT_SERVICE_URL = os.getenv("AIRPORT_SERVICE_URL", "http://localhost:8001")

class AirportServiceAdapter(AirportValidationPort):
    """Adapter que consulta el Airport Service para validar aeropuertos."""

    def __init__(self, timeout: float = 5.0):
        self._timeout = timeout

    def airport_exists(self, airport_id: int) -> bool:
        """Verifica si un aeropuerto existe consultando el Airport Service."""
        try:
            response = httpx.get(
                f"{AIRPORT_SERVICE_URL}/airports/{airport_id}",
                timeout=self._timeout,
            )
            return response.status_code == 200
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return False
            raise RuntimeError(f"Airport Service error: {e.response.status_code}") from e
        except httpx.RequestError as e:
            logger.error("No se pudo conectar al Airport Service: %s", e)
            raise RuntimeError("Airport Service no disponible") from e