"""Custom exceptions for the weather CLI tool."""


class WeatherError(Exception):
    """Base exception for weather-related errors."""
    pass


class LocationError(WeatherError):
    """Exception raised when location cannot be resolved."""
    pass


class WeatherSourceError(WeatherError):
    """Exception raised when weather data source fails."""
    pass


class ConfigError(WeatherError):
    """Exception raised for configuration-related errors."""
    pass


class CacheError(WeatherError):
    """Exception raised for cache-related errors."""
    pass


class FormatError(WeatherError):
    """Exception raised for formatting-related errors."""
    pass


class NetworkError(WeatherError):
    """Exception raised for network-related errors."""
    pass


class ValidationError(WeatherError):
    """Exception raised for validation errors."""
    pass
