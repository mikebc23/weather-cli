"""ASCII art formatter for weather output."""

from typing import List

from ..sources.base import WeatherData
from .base import WeatherFormatter


class VisualFormatter(WeatherFormatter):
    """ASCII art formatter for weather data."""

    def format(self, weather_data: WeatherData) -> str:
        r"""Format weather data with ASCII art.

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
        """Format current weather data with ASCII art."""
        current = weather_data.current
        location = weather_data.location
        units = weather_data.units

        # Prepare data
        location_name = (
            location.name or (f"{location.lat:.4f}, {location.lon:.4f}")
        )
        temp = self._safe_get(current, "temperature_2m")
        temp_unit = units.get("temperature", "°C")
        temperature = f"{temp}{temp_unit}"

        condition = self._safe_get(current, "condition", "Unknown")

        wind_speed = self._safe_get(current, "wind_speed_10m")
        wind_direction_deg = current.get("wind_direction_10m", 0)
        wind_unit = units.get("wind_speed", "km/h")
        wind_str = (
            f"{self._get_wind_arrow(float(wind_direction_deg))} "
            f"{wind_speed} {wind_unit}"
        )

        humidity = self._safe_get(current, "relative_humidity_2m")
        humidity_str = f"{humidity}% humidity"

        # Get weather icon based on condition
        icon = self._get_weather_icon(current.get("weather_code", 0))

        # Build ASCII art
        lines = [
            location_name,
            f"{icon[0]:<13} {temperature}",
            f"{icon[1]:<13} {condition}",
            f"{icon[2]:<13} {wind_str}",
            f"{icon[3]:<13} {humidity_str}",
            icon[4] if len(icon) > 4 else "",
        ]

        # Remove empty lines at the end
        while lines and not lines[-1].strip():
            lines.pop()

        result = "\n".join(lines)

        # Add cache info if this was a cache hit
        if weather_data.cache_hit:
            result += "\n(cached)"

        return result

    def _get_weather_icon(self, weather_code: int) -> List[str]:
        """
        Get ASCII art icon for weather condition.

        Args:
            weather_code: WMO weather code

        Returns:
            List of strings representing ASCII art
        """
        # Clear sky / sunny
        if weather_code == 0:
            return [
                "     \\   /    ",
                "      .-.     ",
                "   ― (   ) ―  ",
                "      `-'     ",
                "     /   \\    ",
            ]

        # Partly cloudy
        elif weather_code in [1, 2]:
            return [
                "   \\  /       ",
                ' _ /"".-.     ',
                "   \\_(   ).   ",
                "   /(___(__) ",
                "             ",
            ]

        # Overcast
        elif weather_code == 3:
            return [
                "             ",
                "     .--.    ",
                "  .-(    ).  ",
                " (___.__)__) ",
                "             ",
            ]

        # Fog
        elif weather_code in [45, 48]:
            return [
                "             ",
                " _ - _ - _ -  ",
                "  _ - _ - _   ",
                " _ - _ - _ -  ",
                "             ",
            ]

        # Rain
        elif weather_code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
            return [
                "     .-.     ",
                "    (   ).   ",
                "   (___(__)  ",
                "    ' ' ' '  ",
                "   ' ' ' '   ",
            ]

        # Snow
        elif weather_code in [71, 73, 75, 77, 85, 86]:
            return [
                "     .-.     ",
                "    (   ).   ",
                "   (___(__)  ",
                "    * * * *  ",
                "   * * * *   ",
            ]

        # Thunderstorm
        elif weather_code in [95, 96, 99]:
            return [
                "     .-.     ",
                "    (   ).   ",
                "   (___(__)  ",
                "    ⚡ ' ⚡  ",
                "   ' ⚡ ' '  ",
            ]

        # Default (unknown)
        else:
            return [
                "     ???     ",
                "    ( ? )    ",
                "   (___?__)  ",
                "     ???     ",
                "             ",
            ]

    def _get_wind_arrow(self, wind_direction_deg: float) -> str:
        """
        Get arrow indicating wind direction.

        Args:
            wind_direction_deg: Wind direction in degrees

        Returns:
            Arrow character indicating wind direction
        """
        # Convert degrees to 8-direction arrows
        arrows = ["↑", "↗", "→", "↘", "↓", "↙", "←", "↖"]
        index = round(wind_direction_deg / 45) % 8
        return arrows[index]

    def _format_hourly(self, weather_data: WeatherData) -> str:
        """Format hourly weather data with simplified visual representation."""
        if not weather_data.hourly_data:
            return "No hourly data available"

        location = weather_data.location
        units = weather_data.units
        
        location_name = (
            location.name or f"{location.lat:.4f}, {location.lon:.4f}"
        )
        
        temp_unit = units.get("temperature", "°C")
        
        # Header
        date_str = weather_data.forecast_date or "Today"
        lines = [
            f"Hourly forecast for {location_name} ({date_str}):",
            "=" * 60,
            ""
        ]
        
        # Hourly entries (simplified for readability)
        for hour_data in weather_data.hourly_data:
            time_str = hour_data.get("time", "")
            if time_str and "T" in time_str:
                hour = time_str.split("T")[1][:5]
            else:
                hour = "N/A"
                
            temp = self._safe_get(hour_data, "temperature_2m")
            condition = self._safe_get(hour_data, "condition", "Unknown")
            humidity = self._safe_get(hour_data, "relative_humidity_2m")
            
            # Simple icon based on condition
            icon = self._get_simple_icon(hour_data.get("weather_code", 0))
            
            line = (
                f"{hour}  {icon}  {temp}{temp_unit}  {condition}  "
                f"({humidity}% humidity)"
            )
            lines.append(line)
        
        return "\n".join(lines)
    
    def _get_simple_icon(self, weather_code: int) -> str:
        """Get a simple icon for weather condition."""
        if weather_code == 0:
            return "☀️"
        elif weather_code in [1, 2]:
            return "⛅"
        elif weather_code == 3:
            return "☁️"
        elif weather_code in [45, 48]:
            return "🌫️"
        elif weather_code in [51, 53, 55, 56, 57]:
            return "🌦️"
        elif weather_code in [61, 63, 65, 66, 67]:
            return "🌧️"
        elif weather_code in [71, 73, 75, 77]:
            return "❄️"
        elif weather_code in [80, 81, 82]:
            return "🌦️"
        elif weather_code in [85, 86]:
            return "🌨️"
        elif weather_code in [95, 96, 99]:
            return "⛈️"
        else:
            return "❓"
