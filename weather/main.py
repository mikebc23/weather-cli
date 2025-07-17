"""Main CLI entry point for the weather tool."""

import argparse
import sys
from typing import Type, Dict
from argparse import Namespace

from .cache import WeatherCache
from .config import WeatherConfig
from .formatters import (
    RawFormatter,
    SimpleFormatter,
    VisualFormatter,
    WeatherFormatter,
)
from .location import LocationResolver
from .sources.open_meteo import OpenMeteoSource
from .utils.exceptions import LocationError, WeatherError, WeatherSourceError


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        prog="weather",
        description="Simple command-line weather tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  weather                                   # Current location (auto-detect)
  weather "New York"                        # City name
  weather "10001"                           # ZIP code
  weather "40.7128,-74.0060"                # Coordinates
  weather --lat=40.7128 --lon=-74.0060      # Explicit coordinates
  weather "London" --format=visual --units=metric
  weather "Tokyo" --source=open-meteo --format=simple
  weather "Rome" --date tomorrow           # Tomorrow's forecast
  weather "Berlin" --date "07252025"       # Specific date (MMDDYYYY)
  weather "Madrid" --hourly                # Hourly forecast
        """,
    )

    # Location arguments
    parser.add_argument(
        "location",
        nargs="?",
        help=(
            "Location (city, ZIP code, coordinates, or "
            "leave empty for auto-detect)"
        ),
    )

    parser.add_argument(
        "--lat", "--latitude", type=float, help="Latitude (use with --lon)"
    )

    parser.add_argument(
        "--lon", "--longitude", type=float, help="Longitude (use with --lat)"
    )

    # Date and time arguments
    parser.add_argument(
        "--date",
        help=(
            "Date for weather data: "
            "MMDDYYYY, today, tomorrow"
        ),
    )

    parser.add_argument(
        "--hourly",
        action="store_true",
        help="Show hourly forecast instead of current conditions",
    )

    # Output format options
    parser.add_argument(
        "--format",
        "-f",
        choices=["simple", "visual", "raw"],
        help="Output format (default: simple)",
    )

    # Unit system
    parser.add_argument(
        "--units",
        "-u",
        choices=["metric", "imperial"],
        help="Unit system (default: metric)",
    )

    # Data source
    parser.add_argument(
        "--source",
        "-s",
        choices=["open-meteo", "wttr", "nws"],
        help="Weather data source (default: open-meteo)",
    )

    # Configuration options
    parser.add_argument("--config", help="Path to configuration file")

    parser.add_argument("--timeout", type=int, help="HTTP timeout in seconds")

    # Cache options
    parser.add_argument(
        "--no-cache", 
        action="store_true", 
        help="Disable cache usage"
    )

    parser.add_argument(
        "--clear-cache", action="store_true", help="Clear cache and exit"
    )

    # Debug options
    parser.add_argument(
        "--version", 
        action="version", 
        version="weather-cli 1.0.0"
    )

    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="Enable debug output"
    )

    return parser


def get_formatter(format_name: str, units: str) -> WeatherFormatter:
    """Get the appropriate formatter instance."""
    formatters: Dict[str, Type[WeatherFormatter]] = {
        "simple": SimpleFormatter,
        "visual": VisualFormatter,
        "raw": RawFormatter,
    }

    formatter_class = formatters.get(format_name)
    if not formatter_class:
        raise WeatherError(f"Unknown format: {format_name}")

    return formatter_class(units=units)


def get_weather_source(source_name: str, timeout: int) -> object:
    """Get the appropriate weather source instance."""
    sources = {
        "open-meteo": OpenMeteoSource,
        # TODO: Add other sources when implemented
        # 'wttr': WttrSource,
        # 'nws': NWSSource
    }

    source_class = sources.get(source_name)
    if not source_class:
        # For now, fallback to open-meteo if other sources aren't implemented
        if source_name in ["wttr", "nws"]:
            print(
                f"Warning: {source_name} source not yet implemented, "
                "using open-meteo",
                file=sys.stderr,
            )
            source_class = OpenMeteoSource
        else:
            raise WeatherError(f"Unknown weather source: {source_name}")

    return source_class(timeout=timeout)


def resolve_location(
    args: Namespace, 
    location_resolver: LocationResolver
) -> object:
    """Resolve location from command line arguments."""
    # Check for explicit coordinates
    if args.lat is not None and args.lon is not None:
        from .location import Coordinates

        return Coordinates(lat=args.lat, lon=args.lon)

    # Check for incomplete coordinate specification
    if args.lat is not None or args.lon is not None:
        raise LocationError("Both --lat and --lon must be specified together")

    # Use location argument or auto-detect
    return location_resolver.resolve(args.location)


def main() -> int:
    """Main CLI entry point."""
    try:
        # Parse command line arguments
        parser = create_parser()
        args = parser.parse_args()

        # Handle special actions
        if args.clear_cache:
            cache = WeatherCache()
            cache.clear()
            print("Cache cleared.")
            return 0

        # Load configuration
        config = WeatherConfig(config_file=args.config)

        # Update config with command line arguments
        config.update_from_args(vars(args))

        # Get configuration values
        format_name = args.format or config.get("format")
        units = args.units or config.get("units")
        source_name = args.source or config.get("source")
        timeout = args.timeout or config.get("timeout")
        use_cache = not args.no_cache

        # Parse date input (NEW)
        from .utils.date_utils import DateParser
        
        target_date = None
        query_type = "current"
        
        if args.date:
            target_date, query_type = DateParser.parse_date_input(args.date)
            DateParser.validate_date_range(target_date)

        if args.debug:
            print(
                f"Debug: Using format={format_name}, units={units}, "
                f"source={source_name}",
                file=sys.stderr,
            )
            if args.date:
                print(
                    f"Debug: Date: {args.date} -> "
                    f"{DateParser.format_date(target_date)} ({query_type})",
                    file=sys.stderr,
                )

        # Initialize components
        location_resolver = LocationResolver(timeout=timeout)
        weather_source = get_weather_source(source_name, timeout)
        formatter = get_formatter(format_name, units)

        # Resolve location
        location = resolve_location(args, location_resolver)

        if args.debug:
            print(f"Debug: Resolved location: {location}", file=sys.stderr)

        # Check cache first (if enabled and current weather only)
        weather_data = None
        use_cache_for_request = use_cache and query_type == "current" and not args.hourly
        
        if use_cache_for_request:
            cache = WeatherCache(
                cache_dir=config.get_cache_dir(),
                cache_duration=config.get("cache_duration"),
            )

            # Create cache key from location
            cache_key = str(location)
            cached_data = cache.get(cache_key, source_name, units)

            if cached_data and args.debug:
                print("Debug: Using cached data", file=sys.stderr)

            # Convert cached dictionary back to WeatherData object
            if cached_data:
                from .sources.base import WeatherData
                
                weather_data = WeatherData(
                    location=location,
                    current=cached_data.get("current", {}),
                    units=cached_data.get("units", {}),
                    source=cached_data.get("source", source_name),
                    timestamp=cached_data.get("timestamp", ""),
                    cache_hit=True,
                    forecast_type=cached_data.get("forecast_type", "current"),
                    forecast_date=cached_data.get("forecast_date"),
                    hourly_data=cached_data.get("hourly_data"),
                )

        # Get fresh data if not cached
        if weather_data is None:
            if args.debug:
                print("Debug: Fetching fresh weather data", file=sys.stderr)

            # Pass date and hourly parameters to source
            weather_data = weather_source.get_weather(  # type: ignore
                location, units, target_date, args.hourly
            )

            # Cache the result (if caching enabled and current weather)
            if use_cache_for_request:
                cache_key = str(location)
                cache.set(
                    cache_key,
                    source_name,
                    units,
                    weather_data.to_dict(),
                )

        # Format and display the result
        output = formatter.format(weather_data)
        print(output)

        return 0

    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        return 130

    except LocationError as e:
        print(f"Location error: {e}", file=sys.stderr)
        return 2

    except WeatherSourceError as e:
        print(f"Weather data error: {e}", file=sys.stderr)
        return 3

    except WeatherError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    except Exception as e:
        if args.debug if "args" in locals() else False:
            import traceback

            traceback.print_exc()
        else:
            print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
