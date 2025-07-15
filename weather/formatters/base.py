"""Base class for weather output formatters."""

from abc import ABC, abstractmethod

class WeatherFormatter(ABC):
    """Abstract base class for weather output formatters."""
    
    @abstractmethod
    def format(self, weather_data) -> str:
        """Format weather data for display."""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get formatter name."""
        pass
