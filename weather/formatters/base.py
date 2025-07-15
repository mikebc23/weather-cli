"""Abstract base class for weather output formatters."""

from abc import ABC, abstractmethod
from ..sources.base import WeatherData


class WeatherFormatter(ABC):
    """Abstract base class for formatting weather data output."""
    
    def __init__(self, units: str = "metric"):
        """
        Initialize formatter with unit system.
        
        Args:
            units: Unit system ('metric' or 'imperial')
        """
        self.units = units
    
    @abstractmethod
    def format(self, weather_data: WeatherData) -> str:
        """
        Format weather data for display.
        
        Args:
            weather_data: Weather data to format
            
        Returns:
            Formatted string for display
        """
        pass
    
    def get_formatter_name(self) -> str:
        """Get the name of this formatter."""
        return self.__class__.__name__.replace('Formatter', '').lower()
    
    def _safe_get(self, data: dict, key: str, default: str = "N/A") -> str:
        """
        Safely get value from dictionary with default.
        
        Args:
            data: Dictionary to get value from
            key: Key to look up
            default: Default value if key not found or value is None
            
        Returns:
            String representation of value or default
        """
        value = data.get(key)
        if value is None:
            return default
        
        # Format numbers to reasonable precision
        if isinstance(value, float):
            return f"{value:.1f}"
        
        return str(value)
    
    def _format_wind_direction(self, degrees: float) -> str:
        """
        Convert wind direction in degrees to compass direction.
        
        Args:
            degrees: Wind direction in degrees
            
        Returns:
            Compass direction (N, NE, E, etc.)
        """
        if degrees is None:
            return "N/A"
        
        directions = [
            "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
        ]
        
        index = round(degrees / 22.5) % 16
        return directions[index]
