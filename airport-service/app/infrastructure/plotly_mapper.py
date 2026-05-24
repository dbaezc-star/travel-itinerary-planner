from typing import List
from app.domain.models import Airport

def to_plotly_format(airports: List[Airport]) -> dict:
    return {
        'type': 'scattergeo',
        'mode': 'markers',
        'lat': [a.longitude for a in airports],
        'lon': [a.latitude for a in airports],
        'text': [a.name for a in airports],
        'customdata': [
            {'id': a.id, 'city': a.city, 'department': a.department, 'iata': a.iata_code or 'N/A'}
            for a in airports
        ],
        'marker': {'size': 10, 'color': '#E8593C', 'symbol': 'circle'},
        'hovertemplate': '<b>%{text}</b><br>Ciudad: %{customdata.city}<br>IATA: %{customdata.iata}<extra></extra>',
    }
