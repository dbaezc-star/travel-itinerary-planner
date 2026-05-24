from fastapi import APIRouter, HTTPException
from app.domain.ports import AirportPort
from app.infrastructure.plotly_mapper import to_plotly_format

router = APIRouter(prefix="/airports", tags=["airports"])

def get_router(port: AirportPort) -> APIRouter:
    """Crea el router inyectando el puerto de dominio."""

    @router.get("/", summary="Listar todos los aeropuertos colombianos")
    def list_airports():
        try:
            airports = port.get_all()
            return [a.to_dict() for a in airports]
        except RuntimeError as e:
            raise HTTPException(status_code=502, detail=str(e))

    @router.get("/map-data", summary="Datos para el mapa Plotly JS")
    def map_data():
        try:
            airports = port.get_all()
            return to_plotly_format(airports)
        except RuntimeError as e:
            raise HTTPException(status_code=502, detail=str(e))

    @router.get("/{airport_id}", summary="Obtener aeropuerto por ID")
    def get_airport(airport_id: int):
        try:
            airport = port.get_by_id(airport_id)
        except RuntimeError as e:
            raise HTTPException(status_code=502, detail=str(e))
        if not airport:
            raise HTTPException(
                status_code=404,
                detail=f"Aeropuerto {airport_id} no encontrado"
            )
        return airport.to_dict()

    return router