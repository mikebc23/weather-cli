"""Test configuration for pytest."""

import pytest
from pathlib import Path
import tempfile
import shutil

from weather.config import WeatherConfig
from weather.cache import WeatherCache
from weather.location import LocationResolver, Coordinates


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def test_config(temp_dir):
    """Create a test configuration."""
    config_file = temp_dir / "test_weather.conf"
    config = WeatherConfig(config_file=str(config_file))
    return config


@pytest.fixture
def test_cache(temp_dir):
    """Create a test cache."""
    cache_dir = temp_dir / "test_cache"
    cache = WeatherCache(cache_dir=str(cache_dir), cache_duration=300)
    return cache


@pytest.fixture
def test_location_resolver():
    """Create a test location resolver."""
    return LocationResolver(timeout=5)


@pytest.fixture
def sample_coordinates():
    """Sample coordinates for testing."""
    return Coordinates(
        lat=40.7128,
        lon=-74.0060,
        name="New York, NY",
        country="US"
    )
