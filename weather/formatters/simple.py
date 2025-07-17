"""Minimal text formatter for weather output."""

from ..sources.base import WeatherData
from .base import WeatherFormatter


class SimpleFormatter(WeatherFormatter):
    """Simple text formatter for weather data."""

    def format(self, weather_data: WeatherData) -> str:
        """
        Format weather data in simple text format.

        Args:
            weather_data: Weather data to format

        Returns:
            Formatted string for display
        """
        # Handle hourly data
        if weather_data.forecast_type == "hourly" and weather_data.hourly_data:
            return self._format_hourly(weather_data)
        
        # Handle current/historical/forecast data
        return self._format_current(weather_data)

    def _format_current(self, weather_data: WeatherData) -> str:
        """Format current weather data."""
        current = weather_data.current
        location = weather_data.location
        units = weather_data.units

        # First line: Location, temperature, condition
        location_name = (
            location.name or f"{location.lat:.4f}, {location.lon:.4f}"
        )
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

    def _format_hourly(self, weather_data: WeatherData) -> str:
        """Format hourly weather data."""
        if not weather_data.hourly_data:
            return "No hourly data available"

        location = weather_data.location
        units = weather_data.units
        
        location_name = (
            location.name or f"{location.lat:.4f}, {location.lon:.4f}"
        )
        
        temp_unit = units.get("temperature", "°C")
        wind_unit = units.get("wind_speed", "km/h")
        
        # Header
        date_str = weather_data.forecast_date or "Today"
        lines = [f"Hourly forecast for {location_name} ({date_str}):", ""]
        
        # Hourly entries
        for hour_data in weather_data.hourly_data:
            time_str = hour_data.get("time", "")
            if time_str:
                # Extract hour from ISO format
                if "T" in time_str:
                    hour = time_str.split("T")[1][:5]
                else:
                    hour = time_str
            else:
                hour = "N/A"
                
            temp = self._safe_get(hour_data, "temperature_2m")
            condition = self._safe_get(hour_data, "condition", "Unknown")
            wind = self._safe_get(hour_data, "wind_speed_10m")
            humidity = self._safe_get(hour_data, "relative_humidity_2m")
            
            line = (
                f"{hour}: {temp}{temp_unit}, {condition} | "
                f"Wind: {wind} {wind_unit} | Humidity: {humidity}%"
            )
            lines.append(line)
        
        return "\n".join(lines)
