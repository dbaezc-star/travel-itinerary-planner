from typing import List
from app.domain.models import Airport

def to_plotly_format(airports: List[Airport]) -> dict:
    """Transforma la lista de aeropuertos al formato que consume Plotly JS."""
    return {
        "type": "scattergeo",
        "mode": "markers+text",
        "lat": [a.latitude for a in airports],
        "lon": [a.longitude for a in airports],
        "text": [a.name for a in airports],
        "customdata": [
            {
                "id": a.id,
                "city": a.city,
                "department": a.department,
                "iata": a.iata_code
            }
            for a in airports
        ],
        "marker": {"size": 8, "color": "#E8593C", "symbol": "circle"},
        "hovertemplate": (
            "<b>%{text}</b><br>"
            "Ciudad: %{customdata.city}<br>"
            "Dpto: %{customdata.department}<br>"
            "IATA: %{customdata.iata}<extra></extra>"
        ),
    }