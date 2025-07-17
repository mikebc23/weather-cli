"""Open-Meteo weather data source."""

from datetime import datetime, timezone
from typing import Optional

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

    def get_weather(
        self,
        location: Coordinates,
        units: str = "metric",
        date: Optional[datetime] = None,
        hourly: bool = False,
    ) -> WeatherData:
        """
        Get weather data from Open-Meteo API.

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
        try:
            # Determine API endpoint and parameters based on date
            if date and date.date() < datetime.now().date():
                # Historical data
                api_url = "https://archive-api.open-meteo.com/v1/archive"
                start_date = end_date = date.strftime("%Y-%m-%d")
            else:
                # Current or forecast data
                api_url = self.BASE_URL
                start_date = end_date = None

            # Prepare API parameters
            params = {
                "latitude": location.lat,
                "longitude": location.lon,
            }

            # Add date parameters for historical data
            if start_date:
                params.update(
                    {
                        "start_date": start_date,
                        "end_date": end_date,
                    }
                )

            # Configure data fields based on hourly vs current
            if hourly:
                params["hourly"] = [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "apparent_temperature",
                    "weather_code",
                    "wind_speed_10m",
                    "wind_direction_10m",
                    "pressure_msl",
                    "cloud_cover",
                ]
                forecast_type = "hourly"
            else:
                params["current"] = [
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
                ]
                forecast_type = (
                    "historical"
                    if date and date.date() < datetime.now().date()
                    else "current"
                )

            # Add common parameters
            params.update(
                {
                    "timezone": "auto",
                }
            )

            # Add forecast days for future dates
            if not start_date:
                params["forecast_days"] = 1

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
            response = self.http_client.get(api_url, params=params)

            # Parse response
            if "error" in response:
                raise WeatherSourceError(f"Open-Meteo API error: {response['error']}")

            # Set units based on the API response
            units_dict = {
                "temperature": "°F" if units == "imperial" else "°C",
                "humidity": "%",
                "wind_speed": "mph" if units == "imperial" else "km/h",
                "pressure": "hPa",
                "visibility": "m",
                "precipitation": "inch" if units == "imperial" else "mm",
            }

            # Determine forecast type
            if hourly:
                forecast_type = "hourly"
            elif date and date.date() < datetime.now().date():
                forecast_type = "historical"
            elif date and date.date() > datetime.now().date():
                forecast_type = "forecast"
            else:
                forecast_type = "current"

            # Process hourly data if requested
            hourly_data_list = None
            if hourly and "hourly" in response:
                hourly_data_list = self._process_hourly_data(response["hourly"], date)

            # Process current/daily data
            if hourly and hourly_data_list:
                # For hourly requests, use first hour as current
                current_weather = hourly_data_list[0] if hourly_data_list else {}
            else:
                # Use current data from API
                current_data = response.get("current", {})
                weather_code = current_data.get("weather_code", 0)
                condition = self._weather_code_to_condition(weather_code)

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
                }

            return WeatherData(
                location=location,
                current=current_weather,
                units=units_dict,
                source="open-meteo",
                timestamp=datetime.now(timezone.utc).isoformat(),
                cache_hit=False,
                forecast_type=forecast_type,
                forecast_date=date.strftime("%Y-%m-%d") if date else None,
                hourly_data=hourly_data_list,
            )

        except Exception as e:
            if isinstance(e, WeatherSourceError):
                raise
            raise WeatherSourceError(
                f"Failed to get weather from Open-Meteo: {e}"
            ) from e

    def _process_hourly_data(self, hourly_data, target_date=None):
        """Process hourly data from API response."""
        if not hourly_data or "time" not in hourly_data:
            return []

        times = hourly_data["time"]
        processed_hours = []

        for i, time_str in enumerate(times):
            # Skip if we have a target date and this hour isn't on that date
            if target_date:
                hour_date = datetime.fromisoformat(time_str).date()
                if hour_date != target_date.date():
                    continue

            weather_code = hourly_data.get("weather_code", [0] * len(times))[i]
            condition = self._weather_code_to_condition(weather_code)

            # Get default lists for missing data
            none_list = [None] * len(times)

            hour_data = {
                "time": time_str,
                "temperature_2m": hourly_data.get("temperature_2m", none_list)[i],
                "relative_humidity_2m": hourly_data.get(
                    "relative_humidity_2m", none_list
                )[i],
                "apparent_temperature": hourly_data.get(
                    "apparent_temperature", none_list
                )[i],
                "wind_speed_10m": hourly_data.get("wind_speed_10m", none_list)[i],
                "wind_direction_10m": hourly_data.get("wind_direction_10m", none_list)[
                    i
                ],
                "pressure_msl": hourly_data.get("pressure_msl", none_list)[i],
                "cloud_cover": hourly_data.get("cloud_cover", none_list)[i],
                "weather_code": weather_code,
                "condition": condition,
            }
            processed_hours.append(hour_data)

        return processed_hours

    def supports_historical(self) -> bool:
        """Return whether source supports historical data."""
        return True

    def supports_forecast(self) -> bool:
        """Return whether source supports forecast data."""
        return True

    def supports_hourly(self) -> bool:
        """Return whether source supports hourly data."""
        return True

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
