from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.api_colombia_adapter import APIColombiaAdapter
from app.api.routes import get_router

app = FastAPI(
    title="Airport Service",
    description="Microservicio de aeropuertos colombianos con patrón Adapter y arquitectura hexagonal.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

adapter = APIColombiaAdapter()
app.include_router(get_router(adapter))

@app.get("/health", tags=["health"])
def health():
    """Verificación de estado del servicio."""
    return {"status": "ok", "service": "airport-service"}