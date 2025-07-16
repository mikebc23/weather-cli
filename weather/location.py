"""Location detection and geocoding services."""

import re
from dataclasses import dataclass
from typing import Optional

import requests

from .utils.exceptions import LocationError


@dataclass
class Coordinates:
    """Represents a geographic coordinate pair."""

    lat: float
    lon: float
    name: Optional[str] = None
    country: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate coordinates after initialization."""
        self._validate()

    def _validate(self):
        """Validate latitude and longitude ranges."""
        if not (-90 <= self.lat <= 90):
            raise LocationError(
                f"Invalid latitude: {self.lat}. Must be between -90 and 90"
            )

        if not (-180 <= self.lon <= 180):
            raise LocationError(
                f"Invalid longitude: {self.lon}. Must be between -180 and 180"
            )

    def normalize_for_cache(self) -> str:
        """Create a normalized string for cache keys."""
        return f"{self.lat:.4f},{self.lon:.4f}"

    def __str__(self) -> str:
        """String representation of coordinates."""
        if self.name:
            return f"{self.name} ({self.lat:.4f}, {self.lon:.4f})"
        return f"{self.lat:.4f}, {self.lon:.4f}"


class LocationResolver:
    """Handles location detection, geocoding, and coordinate parsing."""

    def __init__(self, timeout: int = 10):
        """Initialize location resolver with HTTP timeout."""
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": "weather-cli/1.0.0 (https://github.com/user/weather-cli)"}
        )

    def resolve(self, input_str: Optional[str] = None) -> Coordinates:
        """
        Main entry point - detects type and resolves to coordinates.

        Args:
            input_str: Location input (None for auto-detection)

        Returns:
            Coordinates object

        Raises:
            LocationError: If location cannot be resolved
        """
        if input_str is None:
            return self._detect_current_location()

        input_str = input_str.strip()
        if not input_str:
            return self._detect_current_location()

        location_type = self._detect_location_type(input_str)

        if location_type == "coordinates":
            return self._parse_coordinates(input_str)
        elif location_type == "dms_coordinates":
            return self._parse_dms_coordinates(input_str)
        elif location_type == "zipcode":
            return self._geocode_zipcode(input_str)
        elif location_type == "place_name":
            return self._geocode_place(input_str)
        else:
            raise LocationError(f"Unknown location type for input: {input_str}")

    def _detect_location_type(self, input_str: str) -> str:
        """
        Detect the type of location input.

        Args:
            input_str: Input string to analyze

        Returns:
            Location type: 'coordinates', 'dms_coordinates', 'zipcode', or 'place_name'
        """
        # Remove whitespace for pattern matching
        clean_input = input_str.strip()

        # Decimal coordinates: "40.7128,-74.0060" or "40.7128 -74.0060"
        if re.match(r"^-?\d+\.?\d*[,\s]+-?\d+\.?\d*$", clean_input):
            return "coordinates"

        # US ZIP codes: "10001" or "10001-1234"
        if re.match(r"^\d{5}(-\d{4})?$", clean_input):
            return "zipcode"

        # Degrees, minutes, seconds: contains degree symbols
        if "°" in clean_input or "'" in clean_input or '"' in clean_input:
            return "dms_coordinates"

        # Everything else is treated as a place name
        return "place_name"

    def _parse_coordinates(self, input_str: str) -> Coordinates:
        """
        Parse decimal degree coordinates.

        Args:
            input_str: Coordinate string like "40.7128,-74.0060"

        Returns:
            Coordinates object

        Raises:
            LocationError: If coordinates cannot be parsed
        """
        try:
            # Handle both comma and space separators
            if "," in input_str:
                parts = input_str.split(",")
            else:
                parts = input_str.split()

            if len(parts) != 2:
                raise LocationError(
                    f"Invalid coordinate format: {input_str}. Expected 'lat,lon' or 'lat lon'"
                )

            lat = float(parts[0].strip())
            lon = float(parts[1].strip())

            return Coordinates(lat=lat, lon=lon)

        except ValueError as e:
            raise LocationError(
                f"Invalid coordinate values: {input_str}. Must be numbers"
            ) from e

    def _parse_dms_coordinates(self, input_str: str) -> Coordinates:
        r"""Parse degrees, minutes, seconds coordinates.

        Args:
            input_str: DMS string like "40°42'46.0\"N 74°00'21.6\"W"

        Returns:
            Coordinates object

        Raises:
            LocationError: If DMS coordinates cannot be parsed
        """
        try:
            # Pattern for DMS: 40°42'46.0"N 74°00'21.6"W
            pattern = r"""
                (\d+)°                    # degrees
                (?:(\d+)')?               # minutes (optional)
                (?:(\d+(?:\.\d+)?)\")?    # seconds (optional)
                ([NSEW])                  # direction
            """

            matches = re.findall(pattern, input_str.replace(" ", ""), re.VERBOSE)

            if len(matches) != 2:
                raise LocationError(f"Invalid DMS format: {input_str}")

            def dms_to_decimal(degrees, minutes, seconds, direction):
                """Convert DMS to decimal degrees."""
                deg = float(degrees)
                min_val = float(minutes) if minutes else 0
                sec_val = float(seconds) if seconds else 0

                decimal = deg + (min_val / 60) + (sec_val / 3600)

                if direction in ["S", "W"]:
                    decimal = -decimal

                return decimal

            # Parse latitude and longitude
            lat_match = next((m for m in matches if m[3] in ["N", "S"]), None)
            lon_match = next((m for m in matches if m[3] in ["E", "W"]), None)

            if not lat_match or not lon_match:
                raise LocationError(
                    f"Could not find both latitude and longitude in: {input_str}"
                )

            lat = dms_to_decimal(*lat_match)
            lon = dms_to_decimal(*lon_match)

            return Coordinates(lat=lat, lon=lon)

        except (ValueError, AttributeError) as e:
            raise LocationError(f"Invalid DMS coordinates: {input_str}") from e

    def _geocode_zipcode(self, zipcode: str) -> Coordinates:
        """
        Geocode US ZIP code to coordinates.

        Args:
            zipcode: US ZIP code (5 or 9 digits)

        Returns:
            Coordinates object

        Raises:
            LocationError: If ZIP code cannot be geocoded
        """
        try:
            # Use OpenStreetMap Nominatim for ZIP code geocoding
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                "postalcode": zipcode,
                "country": "US",
                "format": "json",
                "limit": 1,
                "addressdetails": 1,
            }

            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()

            if not data:
                raise LocationError(f"ZIP code not found: {zipcode}")

            result = data[0]
            lat = float(result["lat"])
            lon = float(result["lon"])

            # Extract location name from address
            address = result.get("address", {})
            city = address.get("city") or address.get("town") or address.get("village")
            state = address.get("state")

            name = f"{city}, {state}" if city and state else zipcode

            return Coordinates(lat=lat, lon=lon, name=name, country="US")

        except requests.RequestException as e:
            raise LocationError(f"Failed to geocode ZIP code {zipcode}: {e}") from e
        except (KeyError, ValueError) as e:
            raise LocationError(
                f"Invalid geocoding response for ZIP code {zipcode}"
            ) from e

    def _geocode_place(self, place_name: str) -> Coordinates:
        """
        Geocode place name to coordinates.

        Args:
            place_name: City, country, or address

        Returns:
            Coordinates object

        Raises:
            LocationError: If place cannot be geocoded
        """
        try:
            # Use OpenStreetMap Nominatim for place geocoding
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                "q": place_name,
                "format": "json",
                "limit": 1,
                "addressdetails": 1,
            }

            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()

            if not data:
                raise LocationError(f"Place not found: {place_name}")

            result = data[0]
            lat = float(result["lat"])
            lon = float(result["lon"])

            # Extract structured location information
            address = result.get("address", {})
            display_name = result.get("display_name", place_name)

            # Try to get a clean location name
            city = (
                address.get("city")
                or address.get("town")
                or address.get("village")
                or address.get("municipality")
            )

            country = address.get("country")

            if city and country:
                name = f"{city}, {country}"
            else:
                # Fallback to first two parts of display_name
                parts = display_name.split(", ")
                name = ", ".join(parts[:2]) if len(parts) >= 2 else display_name

            return Coordinates(lat=lat, lon=lon, name=name, country=country)

        except requests.RequestException as e:
            raise LocationError(f"Failed to geocode place {place_name}: {e}") from e
        except (KeyError, ValueError) as e:
            raise LocationError(
                f"Invalid geocoding response for place {place_name}"
            ) from e

    def _detect_current_location(self) -> Coordinates:
        """
        Detect current location using IP geolocation.

        Returns:
            Coordinates object

        Raises:
            LocationError: If location cannot be detected
        """
        try:
            # Use ipapi.co for IP geolocation (free, no API key required)
            url = "https://ipapi.co/json/"

            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()

            if "error" in data:
                raise LocationError(f"IP geolocation failed: {data['error']}")

            lat = float(data["latitude"])
            lon = float(data["longitude"])

            city = data.get("city", "Unknown")
            country = data.get("country_name", "Unknown")

            name = f"{city}, {country}"

            return Coordinates(lat=lat, lon=lon, name=name, country=country)

        except requests.RequestException as e:
            raise LocationError(f"Failed to detect current location: {e}") from e
        except (KeyError, ValueError) as e:
            raise LocationError("Invalid IP geolocation response") from e


# Utility functions for external use
def is_zipcode(input_str: str) -> bool:
    """Check if input string is a US ZIP code."""
    return re.match(r"^\d{5}(-\d{4})?$", input_str.strip()) is not None


def is_coordinates(input_str: str) -> bool:
    """Check if input string contains decimal coordinates."""
    return re.match(r"^-?\d+\.?\d*[,\s]+-?\d+\.?\d*$", input_str.strip()) is not None


def is_dms_coordinates(input_str: str) -> bool:
    """Check if input string contains DMS coordinates."""
    return "°" in input_str or "'" in input_str or '"' in input_str


# Example usage and testing
if __name__ == "__main__":
    # Test the location resolver
    resolver = LocationResolver()

    test_cases = [
        "40.7128,-74.0060",  # NYC coordinates
        "9.9281, -84.0907",  # San José, CR coordinates
        "10001",  # NYC ZIP code
        "90210",  # Beverly Hills ZIP code
        "New York",  # City name
        "San José, Costa Rica",  # Full place name
        "40°42'46.0\"N 74°00'21.6\"W",  # DMS coordinates
        None,  # Auto-detect location
    ]

    for test_input in test_cases:
        try:
            coords = resolver.resolve(test_input)
            print(f"Input: {test_input or 'Auto-detect'}")
            print(f"Result: {coords}")
            print(f"Cache key: {coords.normalize_for_cache()}")
            print("-" * 50)
        except LocationError as e:
            print(f"Error with '{test_input}': {e}")
            print("-" * 50)
