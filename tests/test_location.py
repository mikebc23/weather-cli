"""Tests for location detection and geocoding services."""

import pytest

from weather.location import Coordinates, LocationResolver, is_coordinates, is_zipcode
from weather.utils.exceptions import LocationError


class TestCoordinates:
    """Test the Coordinates class."""

    def test_valid_coordinates(self):
        """Test valid coordinate creation."""
        coords = Coordinates(lat=40.7128, lon=-74.0060, name="NYC")
        assert coords.lat == 40.7128
        assert coords.lon == -74.0060
        assert coords.name == "NYC"

    def test_coordinate_validation(self):
        """Test coordinate validation."""
        # Valid coordinates
        Coordinates(lat=0, lon=0)
        Coordinates(lat=90, lon=180)
        Coordinates(lat=-90, lon=-180)

        # Invalid latitude
        with pytest.raises(LocationError):
            Coordinates(lat=91, lon=0)

        with pytest.raises(LocationError):
            Coordinates(lat=-91, lon=0)

        # Invalid longitude
        with pytest.raises(LocationError):
            Coordinates(lat=0, lon=181)

        with pytest.raises(LocationError):
            Coordinates(lat=0, lon=-181)

    def test_normalize_for_cache(self):
        """Test cache key normalization."""
        coords = Coordinates(lat=40.7128456, lon=-74.0060789)
        cache_key = coords.normalize_for_cache()
        assert cache_key == "40.7128,-74.0061"

    def test_string_representation(self):
        """Test string representation."""
        coords = Coordinates(lat=40.7128, lon=-74.0060)
        assert str(coords) == "40.7128, -74.0060"

        coords_with_name = Coordinates(lat=40.7128, lon=-74.0060, name="NYC")
        assert str(coords_with_name) == "NYC (40.7128, -74.0060)"


class TestLocationResolver:
    """Test the LocationResolver class."""

    def test_init(self):
        """Test LocationResolver initialization."""
        resolver = LocationResolver(timeout=5)
        assert resolver.timeout == 5
        assert resolver.session is not None

    def test_detect_location_type(self):
        """Test location type detection."""
        resolver = LocationResolver()

        # Coordinates
        assert resolver._detect_location_type("40.7128,-74.0060") == "coordinates"
        assert resolver._detect_location_type("40.7128 -74.0060") == "coordinates"
        assert resolver._detect_location_type("-90.0, 180.0") == "coordinates"

        # ZIP codes
        assert resolver._detect_location_type("10001") == "zipcode"
        assert resolver._detect_location_type("10001-1234") == "zipcode"

        # DMS coordinates
        assert (
            resolver._detect_location_type("40°42'46.0\"N 74°00'21.6\"W")
            == "dms_coordinates"
        )
        assert resolver._detect_location_type("40°42'N 74°00'W") == "dms_coordinates"

        # Place names
        assert resolver._detect_location_type("New York") == "place_name"
        assert resolver._detect_location_type("San José, Costa Rica") == "place_name"

    def test_parse_coordinates(self):
        """Test coordinate parsing."""
        resolver = LocationResolver()

        # Comma-separated
        coords = resolver._parse_coordinates("40.7128,-74.0060")
        assert coords.lat == 40.7128
        assert coords.lon == -74.0060

        # Space-separated
        coords = resolver._parse_coordinates("40.7128 -74.0060")
        assert coords.lat == 40.7128
        assert coords.lon == -74.0060

        # Invalid format
        with pytest.raises(LocationError):
            resolver._parse_coordinates("40.7128")

        with pytest.raises(LocationError):
            resolver._parse_coordinates("not,numbers")

    def test_parse_dms_coordinates(self):
        """Test DMS coordinate parsing."""
        resolver = LocationResolver()

        # Full DMS
        coords = resolver._parse_dms_coordinates("40°42'46.0\"N 74°00'21.6\"W")
        assert abs(coords.lat - 40.7128) < 0.01
        assert abs(coords.lon - (-74.0060)) < 0.01

        # Degrees only
        coords = resolver._parse_dms_coordinates("40°N 74°W")
        assert coords.lat == 40.0
        assert coords.lon == -74.0

        # Invalid format
        with pytest.raises(LocationError):
            resolver._parse_dms_coordinates("invalid dms")


class TestUtilityFunctions:
    """Test utility functions."""

    def test_is_zipcode(self):
        """Test ZIP code detection."""
        assert is_zipcode("10001") is True
        assert is_zipcode("10001-1234") is True
        assert is_zipcode("  90210  ") is True

        assert is_zipcode("1000") is False  # Too short
        assert is_zipcode("100001") is False  # Too long
        assert is_zipcode("abcde") is False  # Not numeric
        assert is_zipcode("New York") is False

    def test_is_coordinates(self):
        """Test coordinate detection."""
        assert is_coordinates("40.7128,-74.0060") is True
        assert is_coordinates("40.7128 -74.0060") is True
        assert is_coordinates("-90.0, 180.0") is True
        assert is_coordinates("0,0") is True

        assert is_coordinates("New York") is False
        assert is_coordinates("40.7128") is False  # Only one coordinate
        assert is_coordinates("not,numbers") is False
