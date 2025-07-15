# Weather CLI

A minimal, fast, and extensible weather command-line tool.

## Features

- Multiple weather sources (Open-Meteo, wttr.in, NWS)
- Multiple output formats (minimal, table, ASCII art, raw JSON)
- Support for cities, zipcodes, and coordinates
- Automatic location detection
- Smart caching (5-minute cache)
- Configurable units (metric/imperial)

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Basic usage
weather                           # Current location
weather "San José, CR"            # City name
weather "10001"                   # Zipcode
weather "9.9281,-84.0907"         # Coordinates

# With options
weather --format=table --units=metric
weather --source=om --raw         # Raw JSON output
weather --lat=40.7128 --lon=-74.0060
```

## Configuration

Create `~/.weather.conf`:

```ini
[DEFAULT]
units = metric
format = minimal
source = om
```

## Development

```bash
# Install development dependencies
pip install -e .[dev]

# Run tests
pytest

# Run with coverage
pytest --cov=weather
```
