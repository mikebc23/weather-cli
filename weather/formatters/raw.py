"""Raw JSON formatter for weather output."""

import json

from ..sources.base import WeatherData
from .base import WeatherFormatter


class RawFormatter(WeatherFormatter):
    """Raw JSON formatter for weather data."""

    def format(self, weather_data: WeatherData) -> str:
        """
        Format weather data as raw JSON.

        Args:
            weather_data: Weather data to format

        Returns:
            JSON string with all available data
        """
        # Convert to dictionary and format as JSON
        data_dict = weather_data.to_dict()

        return json.dumps(data_dict, indent=2, ensure_ascii=False)
