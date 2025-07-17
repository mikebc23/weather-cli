# Weather CLI

A simple, fast, and feature-rich command-line weather tool with multiple data sources and output formats.

## Features

- 🌍 **Multiple location input types**: City names, ZIP codes, coordinates (decimal & DMS), auto-detection
- 📊 **Multiple output formats**: Simple, visual, raw JSON
- 📐 **Unit systems**: Metric and Imperial units
- 🏃‍♂️ **Fast and lightweight**: Minimal dependencies, quick responses
- 💾 **Smart caching**: 5-minute cache to reduce API calls
- 🌐 **Multiple data sources**: Open-Meteo (implemented), wttr.in and NWS (planned)
- ⚙️ **Configurable**: Config file and command-line options

## Installation

```bash
# Clone the repository
git clone https://github.com/mikebc23/weather-cli.git
cd weather-cli

# Install in development mode
pip install -e .

# Or install from source
pip install .
```

## Quick Start

```bash
# Current location (auto-detect via IP)
weather

# City names
weather "New York"
weather "San José, Costa Rica"
weather "Tokyo"

# Coordinates
weather "40.7128,-74.0060"           # NYC
weather "9.9281,-84.0907"            # San José, CR
weather --lat=51.5074 --lon=-0.1278  # London

# Different output formats
weather "Tokyo" --format=visual
weather "London" --format=simple --units=imperial
weather "NYC" --format=raw        # JSON output
```

## Output Formats

### Simple (default)

```text
San José, CR: 22°C, Partly Cloudy
Feels like: 25°C | Humidity: 65% | Wind: 8 km/h
```

### Visual

```text
San José, CR
     \   /     22°C
      .-.      Partly Cloudy
   ― (   ) ―   ↗ 8 km/h
      `-'      65% humidity
     /   \
```

### Raw JSON

```json
{
  "location": {
    "name": "San José, Costa Rica",
    "latitude": 9.9281,
    "longitude": -84.0907,
    "country": "Costa Rica"
  },
  "current": {
    "temperature_2m": 22.5,
    "relative_humidity_2m": 65,
    "apparent_temperature": 25.1,
    "wind_speed_10m": 8.2,
    "condition": "Partly cloudy",
    "pressure_msl": 1013.2,
    "cloud_cover": 25,
    "uv_index": 3.2
  },
  "units": {
    "temperature": "°C",
    "wind_speed": "km/h",
    "pressure": "hPa"
  },
  "source": "open-meteo",
  "timestamp": "2025-07-14T15:30:00Z",
  "cache_hit": false
}
```

## Command Line Options

```text
weather [location] [options]

Positional Arguments:
  location              Location (city, ZIP code, coordinates, or auto-detect)

Location Options:
  --lat LAT             Latitude (use with --lon)
  --lon LON             Longitude (use with --lat)

Format Options:
  --format FORMAT       Output format: simple, visual, raw (default: simple)
  --units UNITS         Unit system: metric, imperial (default: metric)

Data Source Options:
  --source SOURCE       Weather source: open-meteo, wttr, nws (default: open-meteo)
  --timeout TIMEOUT     HTTP timeout in seconds (default: 10)

Cache Options:
  --no-cache            Disable cache usage
  --clear-cache         Clear cache and exit

Other Options:
  --config CONFIG       Path to configuration file
  --debug               Enable debug output
  --version             Show version
  --help                Show help message
```

## Configuration

The tool uses a configuration file at `~/.weather.conf` (JSON format):

```json
{
  "units": "metric",
  "format": "simple",
  "source": "open-meteo",
  "cache_duration": 300,
  "timeout": 10
}
```

## Supported Location Formats

| Format | Example | Description |
|--------|---------|-------------|
| Auto-detect | `weather` | Uses IP geolocation |
| City name | `"New York"` | City, country, or address |
| ZIP code | `"10001"` | US ZIP codes (5 or 9 digits) |
| Decimal coordinates | `"40.7128,-74.0060"` | Latitude,longitude |
| Explicit coordinates | `--lat=40.7128 --lon=-74.0060` | Separate lat/lon flags |
| DMS coordinates | `"40°42'46.0\"N 74°00'21.6\"W"` | Degrees, minutes, seconds |

## Project Structure

```text
weather-cli/
├── weather/                 # Main package
│   ├── main.py              # CLI entry point
│   ├── config.py            # Configuration management
│   ├── cache.py             # Caching system
│   ├── location.py          # Location services (geocoding)
│   ├── sources/             # Weather data sources
│   │   ├── base.py          # Abstract base class
│   │   ├── open_meteo.py    # Open-Meteo API
│   │   ├── wttr.py          # wttr.in service
│   │   └── nws.py           # National Weather Service
│   ├── formatters/          # Output formatters
│   │   ├── base.py          # Abstract formatter
│   │   ├── simple.py        # Simple text output
│   │   ├── visual.py        # Visual ASCII art format
│   │   └── raw.py           # Raw JSON output
│   └── utils/               # Utility functions
│       ├── http.py          # HTTP client wrapper
│       ├── units.py         # Unit conversions
│       └── exceptions.py    # Custom exceptions
├── tests/                   # Test suite
│   ├── conftest.py          # pytest fixtures
│   └── test_location.py     # Location tests
├── setup.py                 # Package setup
├── requirements.txt         # Dependencies
└── README.md                # This file
```

## Data Sources

### Open-Meteo (Primary)

- **Status**: Implemented and working
- **Coverage**: Global
- **Features**: Current weather, forecasts, no API key required
- **Rate limit**: Generous free tier
- **URL**: https://open-meteo.com/

### wttr.in (Planned)

- **Status**: Placeholder implemented
- **Coverage**: Global
- **Features**: Simple curl-based service, ASCII art built-in
- **Rate limit**: Fair use

### National Weather Service (Planned)

- **Status**: Placeholder implemented
- **Coverage**: United States only
- **Features**: Official US government weather data
- **Rate limit**: None (government API)

## Dependencies

- `requests>=2.25.0` - HTTP requests
- `urllib3>=1.26.0` - HTTP client utilities

Development dependencies:

- `pytest` - Testing framework

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=weather

# Run specific test file
pytest tests/test_location.py -v
```

## Examples

```bash
# Different locations
weather                                   # Auto-detect
weather "Paris, France"                   # City name
weather "90210"                           # ZIP code
weather "35.6762,139.6503"                # Tokyo coordinates

# Different formats and units
weather "London" --format=visual --units=imperial
weather "Moscow" --format=simple --units=metric
weather "Sydney" --format=raw             # JSON output

# Using explicit coordinates
weather --lat=55.7558 --lon=37.6173       # Moscow
weather --lat=-33.8688 --lon=151.2093     # Sydney

# Configuration and caching
weather "NYC" --no-cache                  # Skip cache
weather --clear-cache                     # Clear cache
weather "NYC" --timeout=5                 # Custom timeout
```

## Error Handling

The tool provides clear error messages for common issues:

- **Location not found**: "Location error: Place not found: Invalid City"
- **Invalid coordinates**: "Location error: Invalid latitude: 91.0. Must be between -90 and 90"
- **Network issues**: "Weather data error: Failed to get weather from Open-Meteo: Connection timeout"
- **Invalid format**: "Error: Unknown format: badformat"

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for your changes
5. Run tests (`pytest`)
6. Commit your changes (`git commit -am 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Open-Meteo](https://open-meteo.com/) for providing excellent free weather API
- [OpenStreetMap Nominatim](https://nominatim.org/) for geocoding services
- Weather icons inspired by wttr.in ASCII art
