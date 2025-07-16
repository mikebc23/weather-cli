"""Custom exceptions for the weather CLI tool."""


class WeatherError(Exception):
    """Base exception for weather-related errors."""


class LocationError(WeatherError):
    """Exception raised when location cannot be resolved."""


class WeatherSourceError(WeatherError):
    """Exception raised when weather data source fails."""


class ConfigError(WeatherError):
    """Exception raised for configuration-related errors."""


class CacheError(WeatherError):
    """Exception raised for cache-related errors."""


class FormatError(WeatherError):
    """Exception raised for formatting-related errors."""


class NetworkError(WeatherError):
    """Exception raised for network-related errors."""


class ValidationError(WeatherError):
    """Exception raised for validation errors."""
