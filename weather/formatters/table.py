"""Table formatter for weather output."""

from ..sources.base import WeatherData
from .base import WeatherFormatter


class TableFormatter(WeatherFormatter):
    """Table formatter for weather data."""

    def format(self, weather_data: WeatherData) -> str:
        """
        Format weather data in table format.

        Example output:
        Location    | Temp  | Condition    | Feels | Humidity | Wind
        San José CR | 22°C  | Partly Cloudy| 25°C  | 65%      | 8 km/h

        Args:
            weather_data: Weather data to format

        Returns:
            Formatted string for display
        """
        current = weather_data.current
        location = weather_data.location
        units = weather_data.units

        # Prepare data
        location_name = location.name or f"{location.lat:.4f}, {location.lon:.4f}"

        # Truncate location name if too long
        if len(location_name) > 12:
            location_name = location_name[:9] + "..."

        temp = self._safe_get(current, "temperature_2m")
        temp_unit = units.get("temperature", "°C")
        temperature = f"{temp}{temp_unit}"

        condition = self._safe_get(current, "condition", "Unknown")
        # Truncate condition if too long
        if len(condition) > 13:
            condition = condition[:10] + "..."

        feels_like = self._safe_get(current, "apparent_temperature")
        feels_like_temp = f"{feels_like}{temp_unit}"

        humidity = self._safe_get(current, "relative_humidity_2m")
        humidity_str = f"{humidity}%"

        wind_speed = self._safe_get(current, "wind_speed_10m")
        wind_unit = units.get("wind_speed", "km/h")
        wind_str = f"{wind_speed} {wind_unit}"

        # Create table
        header = "Location    | Temp  | Condition    | Feels | Humidity | Wind"
        separator = "-" * len(header)

        # Format row with proper padding
        row = (
            f"{location_name:<11} | "
            f"{temperature:<5} | "
            f"{condition:<12} | "
            f"{feels_like_temp:<5} | "
            f"{humidity_str:<8} | "
            f"{wind_str}"
        )

        result = f"{header}\n{separator}\n{row}"

        # Add cache info if this was a cache hit
        if weather_data.cache_hit:
            result += "\n(cached)"

        return result
