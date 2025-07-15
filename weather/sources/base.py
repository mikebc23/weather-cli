"""Base class for weather data sources."""

from abc import ABC, abstractmethod

class WeatherSource(ABC):
    """Abstract base class for weather data sources."""
    
    @abstractmethod
    def get_weather(self, lat: float, lon: float, units: str):
        """Get essential weather data."""
        pass
    
    @abstractmethod
    def get_weather_raw(self, lat: float, lon: float, units: str):
        """Get complete raw API response."""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get source name."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if source is available."""
        pass
