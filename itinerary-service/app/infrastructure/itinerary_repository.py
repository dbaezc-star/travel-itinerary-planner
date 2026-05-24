from typing import List, Optional
from datetime import datetime
from app.domain.models import Itinerary
from app.domain.ports import ItineraryRepository
from app.infrastructure.database import ItineraryORM, get_session

class SQLItineraryRepository(ItineraryRepository):
    def _to_domain(self, orm: ItineraryORM) -> Itinerary:
        return Itinerary(
            id=orm.id,
            user_name=orm.user_name,
            departure_airport_id=orm.departure_airport_id,
            arrival_airport_id=orm.arrival_airport_id,
            travel_date=orm.travel_date,
            duration_minutes=orm.duration_minutes,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    def save(self, itinerary: Itinerary) -> Itinerary:
        with get_session() as session:
            orm = ItineraryORM(
                user_name=itinerary.user_name,
                departure_airport_id=itinerary.departure_airport_id,
                arrival_airport_id=itinerary.arrival_airport_id,
                travel_date=itinerary.travel_date,
                duration_minutes=itinerary.duration_minutes,
            )
            session.add(orm)
            session.flush()
            session.refresh(orm)
            return self._to_domain(orm)

    def find_all(self) -> List[Itinerary]:
        with get_session() as session:
            rows = session.query(ItineraryORM).order_by(ItineraryORM.travel_date).all()
            return [self._to_domain(r) for r in rows]

    def find_by_id(self, itinerary_id: int) -> Optional[Itinerary]:
        with get_session() as session:
            orm = session.query(ItineraryORM).filter(ItineraryORM.id == itinerary_id).first()
            return self._to_domain(orm) if orm else None

    def update(self, itinerary: Itinerary) -> Itinerary:
        with get_session() as session:
            orm = session.query(ItineraryORM).filter(ItineraryORM.id == itinerary.id).first()
            if not orm:
                raise ValueError(f'Itinerario {itinerary.id} no encontrado')
            orm.user_name = itinerary.user_name
            orm.departure_airport_id = itinerary.departure_airport_id
            orm.arrival_airport_id = itinerary.arrival_airport_id
            orm.travel_date = itinerary.travel_date
            orm.duration_minutes = itinerary.duration_minutes
            orm.updated_at = datetime.utcnow()
            session.flush()
            session.refresh(orm)
            return self._to_domain(orm)

    def delete(self, itinerary_id: int) -> bool:
        with get_session() as session:
            orm = session.query(ItineraryORM).filter(ItineraryORM.id == itinerary_id).first()
            if not orm:
                return False
            session.delete(orm)
            return True
