import pytest
from unittest.mock import MagicMock, patch
from datetime import date
from app.domain.models import Itinerary
from app.infrastructure.itinerary_repository import SQLItineraryRepository

def make_itinerary():
    return Itinerary(
        id=1,
        user_name='David Baez',
        departure_airport_id=1,
        arrival_airport_id=2,
        travel_date=date(2026, 8, 15),
        duration_minutes=90,
    )

def test_itinerary_to_dict():
    it = make_itinerary()
    d = it.to_dict()
    assert d['user_name'] == 'David Baez'
    assert d['duration_minutes'] == 90
    assert d['travel_date'] == '2026-08-15'

def test_itinerary_different_airports():
    it = make_itinerary()
    assert it.departure_airport_id != it.arrival_airport_id

def test_itinerary_optional_fields():
    it = Itinerary(
        user_name='Test',
        departure_airport_id=1,
        arrival_airport_id=2,
        travel_date=date(2026, 8, 15),
        duration_minutes=60,
    )
    assert it.id is None
    assert it.created_at is None

def test_airport_validation_adapter():
    from app.infrastructure.airport_service_adapter import AirportServiceAdapter
    adapter = AirportServiceAdapter()
    with patch('httpx.get') as mock_get:
        mock_get.return_value = MagicMock(status_code=200)
        assert adapter.airport_exists(1) == True

def test_airport_validation_not_found():
    from app.infrastructure.airport_service_adapter import AirportServiceAdapter
    import httpx
    adapter = AirportServiceAdapter()
    with patch('httpx.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.side_effect = httpx.HTTPStatusError('not found', request=MagicMock(), response=mock_response)
        assert adapter.airport_exists(999) == False
