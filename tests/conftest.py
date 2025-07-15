"""Pytest configuration and fixtures."""

import pytest

@pytest.fixture
def mock_weather_response():
    """Mock weather API response."""
    return {
        "current": {
            "temperature_2m": 22.5,
            "relative_humidity_2m": 65,
            "wind_speed_10m": 8.2,
            "weather_code": 1,
            "pressure_msl": 1013.2,
            "cloud_cover": 25,
            "visibility": 10000,
            "uv_index": 3.2,
            "dewpoint_2m": 15.8
        }
    }

@pytest.fixture
def sample_coordinates():
    """Sample coordinates for testing."""
    return {
        "san_jose_cr": (9.9281, -84.0907),
        "new_york": (40.7128, -74.0060),
        "london": (51.5074, -0.1278)
    }
