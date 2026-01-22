from celery import shared_task
from venues.models import Venue
from weather.models import WeatherSnapshot
from weather.services import fetch_weather_for_venue

@shared_task
def update_weather_snapshots():
    """
    Периодическая задача: пробегается по всем Venues и сохраняет погоду.
    """
    venues = Venue.objects.all()
    results = []
    for venue in venues:
        weather_data = fetch_weather_for_venue(venue)
        if weather_data:
            WeatherSnapshot.objects.create(venue=venue, **weather_data)
            results.append(f"Updated {venue.name}")
        else:
            results.append(f"Failed {venue.name}")
    return results
