"""wttr.in weather data source (placeholder)."""

from .base import WeatherSource, WeatherData
from ..location import Coordinates
from ..utils.exceptions import WeatherSourceError


class WttrSource(WeatherSource):
    """Weather data source using wttr.in service."""
    
    def __init__(self, timeout: int = 10):
        """Initialize wttr.in source."""
        super().__init__(timeout)
        # TODO: Implement wttr.in integration
    
    def get_weather(self, location: Coordinates, units: str = "metric") -> WeatherData:
        """
        Get weather data from wttr.in service.
        
        Args:
            location: Location coordinates
            units: Unit system ('metric' or 'imperial')
            
        Returns:
            WeatherData object
            
        Raises:
            WeatherSourceError: Always raises for now (not implemented)
        """
        raise WeatherSourceError("wttr.in source not yet implemented")
    
    def is_location_supported(self, location: Coordinates) -> bool:
        """
        Check if location is supported by wttr.in.
        
        Args:
            location: Location coordinates
            
        Returns:
            False (not implemented)
        """
        return False
