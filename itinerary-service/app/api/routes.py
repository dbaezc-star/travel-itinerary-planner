from fastapi import APIRouter, HTTPException
from app.api.schemas import ItineraryCreate, ItineraryUpdate, ItineraryResponse
from app.domain.models import Itinerary
from app.domain.ports import ItineraryRepository, AirportValidationPort

router = APIRouter(prefix='/itineraries', tags=['itineraries'])

def _validate_airports(validator: AirportValidationPort, dep_id: int, arr_id: int):
    try:
        if not validator.airport_exists(dep_id):
            raise HTTPException(status_code=422, detail=f'Aeropuerto de salida {dep_id} no existe')
        if not validator.airport_exists(arr_id):
            raise HTTPException(status_code=422, detail=f'Aeropuerto de llegada {arr_id} no existe')
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

def get_router(repo: ItineraryRepository, validator: AirportValidationPort) -> APIRouter:

    @router.post('/', status_code=201, response_model=ItineraryResponse, summary='Crear itinerario')
    def create(body: ItineraryCreate):
        _validate_airports(validator, body.departure_airport_id, body.arrival_airport_id)
        itinerary = Itinerary(
            user_name=body.user_name,
            departure_airport_id=body.departure_airport_id,
            arrival_airport_id=body.arrival_airport_id,
            travel_date=body.travel_date,
            duration_minutes=body.duration_minutes,
        )
        saved = repo.save(itinerary)
        return saved.to_dict()

    @router.get('/', response_model=list[ItineraryResponse], summary='Listar itinerarios')
    def list_all():
        return [i.to_dict() for i in repo.find_all()]

    @router.get('/{itinerary_id}', response_model=ItineraryResponse, summary='Obtener itinerario')
    def get_one(itinerary_id: int):
        item = repo.find_by_id(itinerary_id)
        if not item:
            raise HTTPException(status_code=404, detail=f'Itinerario {itinerary_id} no encontrado')
        return item.to_dict()

    @router.put('/{itinerary_id}', response_model=ItineraryResponse, summary='Actualizar itinerario')
    def update(itinerary_id: int, body: ItineraryUpdate):
        item = repo.find_by_id(itinerary_id)
        if not item:
            raise HTTPException(status_code=404, detail=f'Itinerario {itinerary_id} no encontrado')
        if body.user_name is not None:
            item.user_name = body.user_name
        if body.departure_airport_id is not None:
            item.departure_airport_id = body.departure_airport_id
        if body.arrival_airport_id is not None:
            item.arrival_airport_id = body.arrival_airport_id
        if body.travel_date is not None:
            item.travel_date = body.travel_date
        if body.duration_minutes is not None:
            item.duration_minutes = body.duration_minutes
        _validate_airports(validator, item.departure_airport_id, item.arrival_airport_id)
        updated = repo.update(item)
        return updated.to_dict()

    @router.delete('/{itinerary_id}', summary='Eliminar itinerario')
    def delete(itinerary_id: int):
        deleted = repo.delete(itinerary_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f'Itinerario {itinerary_id} no encontrado')
        return {'message': f'Itinerario {itinerary_id} eliminado exitosamente'}

    return router
