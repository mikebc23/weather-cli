"""Custom exceptions for weather CLI."""

class WeatherError(Exception):
    """Base exception for weather CLI."""
    pass

class LocationError(WeatherError):
    """Exception for location-related errors."""
    pass

class WeatherSourceError(WeatherError):
    """Exception for weather source errors."""
    pass

class ConfigError(WeatherError):
    """Exception for configuration errors."""
    pass
