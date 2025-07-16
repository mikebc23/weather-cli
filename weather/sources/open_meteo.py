"""Open-Meteo weather data source."""

from datetime import datetime, timezone

from ..location import Coordinates
from ..utils.exceptions import WeatherSourceError
from ..utils.http import HTTPClient
from .base import WeatherData, WeatherSource


class OpenMeteoSource(WeatherSource):
    """Weather data source using Open-Meteo API."""

    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, timeout: int = 10):
        """Initialize Open-Meteo source."""
        super().__init__(timeout)
        self.http_client = HTTPClient(timeout=timeout)

    def get_weather(self, location: Coordinates, units: str = "metric") -> WeatherData:
        """
        Get weather data from Open-Meteo API.

        Args:
            location: Location coordinates
            units: Unit system ('metric' or 'imperial')

        Returns:
            WeatherData object

        Raises:
            WeatherSourceError: If weather data cannot be retrieved
        """
        try:
            # Prepare API parameters
            params = {
                "latitude": location.lat,
                "longitude": location.lon,
                "current": [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "apparent_temperature",
                    "weather_code",
                    "wind_speed_10m",
                    "wind_direction_10m",
                    "wind_gusts_10m",
                    "pressure_msl",
                    "surface_pressure",
                    "cloud_cover",
                    "visibility",
                    "uv_index",
                    "precipitation",
                    "rain",
                    "snowfall",
                ],
                "timezone": "auto",
                "forecast_days": 1,
            }

            # Set temperature and wind speed units
            if units == "imperial":
                params["temperature_unit"] = "fahrenheit"
                params["wind_speed_unit"] = "mph"
                params["precipitation_unit"] = "inch"
            else:
                params["temperature_unit"] = "celsius"
                params["wind_speed_unit"] = "kmh"
                params["precipitation_unit"] = "mm"

            # Make API request
            response = self.http_client.get(self.BASE_URL, params=params)

            # Parse response
            if "error" in response:
                raise WeatherSourceError(f"Open-Meteo API error: {response['error']}")

            current_data = response.get("current", {})
            location_data = {
                "latitude": response.get("latitude"),
                "longitude": response.get("longitude"),
                "elevation": response.get("elevation"),
                "timezone": response.get("timezone"),
            }

            # Convert weather code to condition description
            weather_code = current_data.get("weather_code", 0)
            condition = self._weather_code_to_condition(weather_code)

            # Prepare current weather data
            current_weather = {
                "temperature_2m": current_data.get("temperature_2m"),
                "relative_humidity_2m": current_data.get("relative_humidity_2m"),
                "apparent_temperature": current_data.get("apparent_temperature"),
                "wind_speed_10m": current_data.get("wind_speed_10m"),
                "wind_direction_10m": current_data.get("wind_direction_10m"),
                "wind_gusts_10m": current_data.get("wind_gusts_10m"),
                "weather_code": weather_code,
                "condition": condition,
                "pressure_msl": current_data.get("pressure_msl"),
                "surface_pressure": current_data.get("surface_pressure"),
                "cloud_cover": current_data.get("cloud_cover"),
                "visibility": current_data.get("visibility"),
                "uv_index": current_data.get("uv_index"),
                "precipitation": current_data.get("precipitation"),
                "rain": current_data.get("rain"),
                "snowfall": current_data.get("snowfall"),
            }

            # Set units based on the API response
            units_dict = {
                "temperature": "°F" if units == "imperial" else "°C",
                "humidity": "%",
                "wind_speed": "mph" if units == "imperial" else "km/h",
                "pressure": "hPa",
                "visibility": "m",
                "precipitation": "inch" if units == "imperial" else "mm",
            }

            # Update location with additional info if available
            if location_data.get("elevation"):
                # Note: We don't modify the original location object
                pass

            return WeatherData(
                location=location,
                current=current_weather,
                units=units_dict,
                source="open-meteo",
                timestamp=datetime.now(timezone.utc).isoformat(),
                cache_hit=False,
            )

        except Exception as e:
            if isinstance(e, WeatherSourceError):
                raise
            raise WeatherSourceError(
                f"Failed to get weather from Open-Meteo: {e}"
            ) from e

    def is_location_supported(self, location: Coordinates) -> bool:
        """
        Check if location is supported by Open-Meteo.

        Open-Meteo supports global coverage.

        Args:
            location: Location coordinates

        Returns:
            True (Open-Meteo has global coverage)
        """
        return True

    def _weather_code_to_condition(self, code: int) -> str:
        """
        Convert WMO weather code to human-readable condition.

        Args:
            code: WMO weather code

        Returns:
            Human-readable weather condition
        """
        # WMO Weather interpretation codes
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            56: "Light freezing drizzle",
            57: "Dense freezing drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            66: "Light freezing rain",
            67: "Heavy freezing rain",
            71: "Slight snow fall",
            73: "Moderate snow fall",
            75: "Heavy snow fall",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail",
        }

        return weather_codes.get(code, f"Unknown ({code})")
