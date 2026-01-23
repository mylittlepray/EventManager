# weather/services.py
import requests

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def degrees_to_direction(degrees):
    """Преобразует градусы направления ветра в текстовые обозначения."""
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    index = round(degrees / 45) % 8
    return directions[index]

def hpa_to_mmhg(hpa):
    """Преобразует давление из гПа (гектопаскалей) в мм рт.ст."""
    return hpa * 0.75006

def fetch_weather_for_venue(venue):
    """
    Получает текущую погоду для venue через Open-Meteo API.
    Возвращает словарь с данными погоды или None при ошибке.
    """
    lat = venue.location.y
    lon = venue.location.x

    lat = venue.location.y
    lon = venue.location.x

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m,wind_direction_10m"
        f"&timezone=auto"
    )

    session = requests.Session()
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)

    try:
        response = session.get(url, timeout=20)
        response.raise_for_status()
        data = response.json()
        current = data.get("current", {})

        return {
            "temperature_celsius": current.get("temperature_2m", 0.0),
            "humidity_percent": current.get("relative_humidity_2m", 0.0),
            "pressure_mmhg": hpa_to_mmhg(current.get("surface_pressure", 1013.0)),
            "wind_speed_ms": current.get("wind_speed_10m", 0.0),
            "wind_direction": degrees_to_direction(current.get("wind_direction_10m", 0.0)),
        }
    except Exception as e:
        print(f"Error fetching weather for {venue.name}: {e}")
        return None
