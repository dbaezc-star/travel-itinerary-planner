# Travel Itinerary Planner

Sistema de microservicios para planificacion de itinerarios de viaje en Colombia.

## Arquitectura

- **Airport Service** (puerto 8001): Microservicio que consume la API Colombia con patron Adapter
- **Itinerary Service** (puerto 8002): Microservicio CRUD de itinerarios con SQLite y SQLAlchemy
- **Frontend**: Interfaz web con mapa Plotly JS

## Requisitos

- Python 3.11+
- Docker Desktop (opcional)

## Correr localmente

### Airport Service
cd airport-service
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001

### Itinerary Service
cd itinerary-service
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8002

### Frontend
Abrir frontend/index.html en el navegador

## Pruebas unitarias

cd airport-service && python -m pytest tests/ -v
cd itinerary-service && python -m pytest tests/ -v

## Pruebas de carga

pip install locust
cd load-tests
locust -f locustfile.py

## Docker

docker-compose up --build

## Swagger

- Airport Service: http://localhost:8001/docs
- Itinerary Service: http://localhost:8002/docs
