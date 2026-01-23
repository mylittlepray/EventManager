# tests/test_events.py
import pytest
from django.urls import reverse
from events.models import EventStatus

@pytest.mark.django_db
def test_list_events_published_only(api_client, event_factory):
    pub_event = event_factory(status=EventStatus.PUBLISHED)
    draft_event = event_factory(status=EventStatus.DRAFT)
    
    url = reverse('events-list')
    response = api_client.get(url)
    
    assert response.status_code == 200
    assert len(response.data['results']) == 1 
    assert response.data['results'][0]['id'] == pub_event.id

@pytest.mark.django_db
def test_create_event(api_client, user_factory, venue_factory):
    admin = user_factory(is_superuser=True)
    venue = venue_factory()
    api_client.force_authenticate(user=admin)
    
    url = reverse('events-list')
    data = {
        "title": "Mega Party",
        "description": "Best party",
        "start_at": "2026-05-01T20:00:00Z",
        "end_at": "2026-05-01T23:00:00Z",
        "publish_at": "2026-04-01T12:00:00Z",
        "venue": venue.id,
        "status": "PUBLISHED"
    }
    
    response = api_client.post(url, data)
    assert response.status_code == 201
    assert response.data['title'] == "Mega Party"

@pytest.mark.django_db
def test_get_weather_action(api_client, event_factory, mocker):
    mock_weather = mocker.patch('events.views.get_forecast_for_time')
    mock_weather.return_value = {
        "temperature_celsius": 25.0,
        "humidity_percent": 50,
        "pressure_mmhg": 760,
        "wind_speed_ms": 5.0,
        "wind_direction": 180
    }
    
    event = event_factory(status=EventStatus.PUBLISHED)
    
    url = reverse('events-get-weather', args=[event.id])
    response = api_client.get(url)
    
    assert response.status_code == 200
    assert response.data['temperature_celsius'] == 25.0
    mock_weather.assert_called_once()
