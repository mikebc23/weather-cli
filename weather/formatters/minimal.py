"""Minimal text formatter for weather output."""

from ..sources.base import WeatherData
from .base import WeatherFormatter


class MinimalFormatter(WeatherFormatter):
    """Minimal text formatter for weather data."""

    def format(self, weather_data: WeatherData) -> str:
        """
        Format weather data in minimal text format.

        Example output:
        San José, CR: 22°C, Partly Cloudy
        Feels like: 25°C | Humidity: 65% | Wind: 8 km/h

        Args:
            weather_data: Weather data to format

        Returns:
            Formatted string for display
        """
        current = weather_data.current
        location = weather_data.location
        units = weather_data.units

        # First line: Location, temperature, condition
        location_name = location.name or f"{location.lat:.4f}, {location.lon:.4f}"
        temp = self._safe_get(current, "temperature_2m")
        condition = self._safe_get(current, "condition", "Unknown")
        temp_unit = units.get("temperature", "°C")

        line1 = f"{location_name}: {temp}{temp_unit}, {condition}"

        # Second line: Feels like, humidity, wind
        feels_like = self._safe_get(current, "apparent_temperature")
        humidity = self._safe_get(current, "relative_humidity_2m")
        wind_speed = self._safe_get(current, "wind_speed_10m")
        wind_unit = units.get("wind_speed", "km/h")

        line2 = (
            f"Feels like: {feels_like}{temp_unit} | "
            f"Humidity: {humidity}% | "
            f"Wind: {wind_speed} {wind_unit}"
        )

        result = f"{line1}\n{line2}"

        # Add cache info if this was a cache hit
        if weather_data.cache_hit:
            result += "\n(cached)"

        return result
