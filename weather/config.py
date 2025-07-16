"""Configuration management for the weather CLI."""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

from .utils.exceptions import ConfigError


class WeatherConfig:
    """Manages configuration for the weather CLI tool."""

    DEFAULT_CONFIG = {
        "units": "metric",
        "format": "minimal",
        "source": "open-meteo",
        "cache_duration": 300,  # 5 minutes in seconds
        "timeout": 10,  # HTTP timeout in seconds
        "retries": 3,  # HTTP retries
    }

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration.

        Args:
            config_file: Path to config file (default: ~/.weather.conf)
        """
        if config_file:
            self.config_file = Path(config_file)
        else:
            self.config_file = Path.home() / ".weather.conf"

        self.config = self.DEFAULT_CONFIG.copy()
        self.load()

    def load(self) -> None:
        """Load configuration from file."""
        try:
            if self.config_file.exists():
                with open(self.config_file, encoding="utf-8") as f:
                    file_config = json.load(f)

                # Validate and merge configuration
                for key, value in file_config.items():
                    if key in self.DEFAULT_CONFIG:
                        self.config[key] = value
                    else:
                        print(f"Warning: Unknown config option '{key}' ignored")

                # Validate configuration values
                self._validate_config()

        except (json.JSONDecodeError, OSError) as e:
            raise ConfigError(
                f"Failed to load config from {self.config_file}: {e}"
            ) from e

    def save(self) -> None:
        """Save current configuration to file."""
        try:
            # Create config directory if it doesn't exist
            self.config_file.parent.mkdir(parents=True, exist_ok=True)

            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)

        except OSError as e:
            raise ConfigError(
                f"Failed to save config to {self.config_file}: {e}"
            ) from e

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value
        """
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value.

        Args:
            key: Configuration key
            value: Configuration value
        """
        if key not in self.DEFAULT_CONFIG:
            raise ConfigError(f"Unknown configuration key: {key}")

        self.config[key] = value
        self._validate_config()

    def reset(self) -> None:
        """Reset configuration to defaults."""
        self.config = self.DEFAULT_CONFIG.copy()

    def _validate_config(self) -> None:
        """Validate configuration values."""
        # Validate units
        if self.config["units"] not in ["metric", "imperial"]:
            raise ConfigError(
                f"Invalid units: {self.config['units']}. Must be 'metric' or 'imperial'"
            )

        # Validate format
        valid_formats = ["minimal", "table", "ascii", "raw"]
        if self.config["format"] not in valid_formats:
            raise ConfigError(
                f"Invalid format: {self.config['format']}. Must be one of {valid_formats}"
            )

        # Validate source
        valid_sources = ["open-meteo", "wttr", "nws"]
        if self.config["source"] not in valid_sources:
            raise ConfigError(
                f"Invalid source: {self.config['source']}. Must be one of {valid_sources}"
            )

        # Validate numeric values
        if (
            not isinstance(self.config["cache_duration"], int)
            or self.config["cache_duration"] < 0
        ):
            raise ConfigError("cache_duration must be a non-negative integer")

        if not isinstance(self.config["timeout"], int) or self.config["timeout"] <= 0:
            raise ConfigError("timeout must be a positive integer")

        if not isinstance(self.config["retries"], int) or self.config["retries"] < 0:
            raise ConfigError("retries must be a non-negative integer")

    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values."""
        return self.config.copy()

    def update_from_args(self, args: Dict[str, Any]) -> None:
        """
        Update configuration from command line arguments.

        Args:
            args: Dictionary of command line arguments
        """
        # Map command line args to config keys
        arg_mapping = {
            "units": "units",
            "format": "format",
            "source": "source",
            "timeout": "timeout",
        }

        for arg_key, config_key in arg_mapping.items():
            if args.get(arg_key) is not None:
                self.set(config_key, args[arg_key])

    def get_cache_dir(self) -> str:
        """Get cache directory path."""
        cache_dir = os.environ.get("WEATHER_CACHE_DIR")
        if cache_dir:
            return cache_dir
        return str(Path.home() / ".weather_cache")

    def __str__(self) -> str:
        """String representation of configuration."""
        lines = ["Weather CLI Configuration:"]
        for key, value in sorted(self.config.items()):
            lines.append(f"  {key}: {value}")
        lines.append(f"  config_file: {self.config_file}")
        return "\n".join(lines)
