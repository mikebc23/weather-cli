"""National Weather Service API source (placeholder)."""

from ..location import Coordinates
from ..utils.exceptions import WeatherSourceError
from .base import WeatherData, WeatherSource


class NWSSource(WeatherSource):
    """Weather data source using National Weather Service API."""

    def __init__(self, timeout: int = 10):
        """Initialize NWS source."""
        super().__init__(timeout)
        # TODO: Implement NWS API integration

    def get_weather(self, location: Coordinates, units: str = "metric") -> WeatherData:
        """
        Get weather data from NWS API.

        Args:
            location: Location coordinates
            units: Unit system ('metric' or 'imperial')

        Returns:
            WeatherData object

        Raises:
            WeatherSourceError: Always raises for now (not implemented)
        """
        raise WeatherSourceError("NWS source not yet implemented")

    def is_location_supported(self, location: Coordinates) -> bool:
        """
        Check if location is supported by NWS.

        NWS only supports US locations.

        Args:
            location: Location coordinates

        Returns:
            False (not implemented)
        """
        return False
