import pytest
from unittest.mock import patch, MagicMock
from app.domain.models import Airport
from app.infrastructure.api_colombia_adapter import APIColombiaAdapter

def make_airport():
    return Airport(id=1, name='El Dorado', city='Bogota', department='Cundinamarca', latitude=4.7, longitude=-74.1, iata_code='BOG')

def test_translate_valid():
    adapter = APIColombiaAdapter()
    raw = {'id': '1', 'name': 'El Dorado', 'city': {'name': 'Bogota', 'departmentName': 'Cundinamarca'}, 'latitude': '4.7', 'longitude': '-74.1', 'iataCode': 'BOG'}
    result = adapter._translate(raw)
    assert result.name == 'El Dorado'
    assert result.iata_code == 'BOG'

def test_translate_invalid():
    adapter = APIColombiaAdapter()
    result = adapter._translate({})
    assert result is None

def test_get_all_success():
    adapter = APIColombiaAdapter()
    raw = [{'id': '1', 'name': 'El Dorado', 'city': {'name': 'Bogota', 'departmentName': 'Cundinamarca'}, 'latitude': '4.7', 'longitude': '-74.1', 'iataCode': 'BOG'}]
    with patch.object(adapter, '_fetch', return_value=raw):
        result = adapter.get_all()
    assert len(result) == 1
    assert result[0].city == 'Bogota'

def test_get_by_id_not_found():
    adapter = APIColombiaAdapter()
    with patch.object(adapter, '_fetch', return_value=None):
        result = adapter.get_by_id(999)
    assert result is None

def test_airport_to_dict():
    airport = make_airport()
    d = airport.to_dict()
    assert d['id'] == 1
    assert d['iata_code'] == 'BOG'
