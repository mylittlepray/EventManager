# weather/models.py
from django.db import models
from venues.models import Venue

class WeatherSnapshot(models.Model):
    venue = models.ForeignKey(
        Venue,
        on_delete=models.CASCADE,
        related_name="weather_snapshots",
    )

    temperature_celsius = models.FloatField(help_text="Температура в °C")
    humidity_percent = models.FloatField(help_text="Влажность в %")
    pressure_mmhg = models.FloatField(help_text="Давление в мм рт.ст.")
    wind_direction = models.CharField(max_length=10, help_text="Направление ветра (N/NE/E/SE/S/SW/W/NW)")
    wind_speed_ms = models.FloatField(help_text="Скорость ветра в м/с")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Weather at {self.venue.name} on {self.created_at}"
