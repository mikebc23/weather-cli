# weather-cli

A fast, feature-rich command-line weather tool with multiple data sources and output formats.

## Quick Start

```bash
pip install weather-cli
weather "New York"
```

## Features

- 🌍 Multiple location formats (city, coordinates, ZIP codes)
- 📊 Multiple output formats (simple, visual ASCII art, raw JSON)
- 📅 Historical weather data and forecasts
- ⏰ Hourly forecasts with visual timeline
- 🌐 Multiple weather data sources (Open-Meteo)
- 💾 Smart caching for fast responses
- 🎨 Beautiful ASCII art weather displays

## Installation

### PyPI (Recommended)

```bash
pip install weather-cli
```

### Homebrew (macOS)

```bash
brew install weather-cli
```

## Usage

```bash
# Current weather
weather "Boston"

# Tomorrow's forecast
weather "Tokyo" --date tomorrow

# Hourly forecast
weather "London" --hourly

# Visual ASCII art
weather "Paris" --format visual

# Historical data
weather "Berlin" --date "07152025"
```

See the [full documentation](https://github.com/mikebc23/weather-cli) for more examples.
