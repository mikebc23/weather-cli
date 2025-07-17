"""Abstract base class for weather data sources."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..location import Coordinates


@dataclass
class WeatherData:
    """Standard weather data structure."""

    location: Coordinates
    current: Dict[str, Any]
    units: Dict[str, str]
    source: str
    timestamp: str
    cache_hit: bool = False
    
    # New fields for date/hourly support
    forecast_type: str = "current"  # current, historical, forecast, hourly
    forecast_date: Optional[str] = None
    hourly_data: Optional[List[Dict[str, Any]]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "location": {
                "name": self.location.name,
                "latitude": self.location.lat,
                "longitude": self.location.lon,
                "country": self.location.country,
            },
            "current": self.current,
            "units": self.units,
            "source": self.source,
            "timestamp": self.timestamp,
            "cache_hit": self.cache_hit,
            "forecast_type": self.forecast_type,
            "forecast_date": self.forecast_date,
            "hourly_data": self.hourly_data,
        }


class WeatherSource(ABC):
    """Abstract base class for weather data sources."""

    def __init__(self, timeout: int = 10):
        """Initialize weather source with timeout."""
        self.timeout = timeout
        self.name = self.__class__.__name__.replace("Source", "").lower()

    @abstractmethod
    def get_weather(
        self,
        location: Coordinates,
        units: str = "metric",
        date: Optional[datetime] = None,
        hourly: bool = False,
    ) -> WeatherData:
        """
        Get weather data for the specified location.

        Args:
            location: Location coordinates
            units: Unit system ('metric' or 'imperial')
            date: Date for historical/forecast data
            hourly: Whether to return hourly data

        Returns:
            WeatherData object

        Raises:
            WeatherSourceError: If weather data cannot be retrieved
        """

    @abstractmethod
    def is_location_supported(self, location: Coordinates) -> bool:
        """
        Check if the location is supported by this source.

        Args:
            location: Location coordinates

        Returns:
            True if location is supported, False otherwise
        """

    @abstractmethod
    def supports_historical(self) -> bool:
        """Return whether source supports historical data."""
        
    @abstractmethod
    def supports_forecast(self) -> bool:
        """Return whether source supports forecast data."""
        
    @abstractmethod
    def supports_hourly(self) -> bool:
        """Return whether source supports hourly data."""

    def get_source_name(self) -> str:
        """Get the name of this weather source."""
        return self.name

    def __str__(self) -> str:
        """String representation of the weather source."""
        return f"{self.__class__.__name__}(timeout={self.timeout})"
