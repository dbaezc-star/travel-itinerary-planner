from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.database import create_tables
from app.infrastructure.itinerary_repository import SQLItineraryRepository
from app.infrastructure.airport_service_adapter import AirportServiceAdapter
from app.api.routes import get_router

app = FastAPI(
    title='Itinerary Service',
    description='Microservicio CRUD de itinerarios de viaje con validacion de aeropuertos.',
    version='1.0.0',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.on_event('startup')
def startup():
    create_tables()

repo = SQLItineraryRepository()
validator = AirportServiceAdapter()
app.include_router(get_router(repo, validator))

@app.get('/health', tags=['health'])
def health():
    return {'status': 'ok', 'service': 'itinerary-service'}
