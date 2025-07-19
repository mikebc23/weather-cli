# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-07-18

### Added
- Initial release of weather-cli
- Support for current weather conditions
- Multiple output formats: simple, visual, raw JSON
- Historical weather data support
- Weather forecasts and hourly forecasts
- Date-specific queries (today, tomorrow, MMDDYYYY format)
- Multiple location input types (city, coordinates, ZIP codes)
- Smart caching system
- Visual ASCII art weather displays
- Open-Meteo API integration
- Command-line interface with comprehensive options
- Cross-platform support (macOS, Linux, Windows)

### Features
- `weather "City"` - Current weather for any location
- `weather --date tomorrow` - Tomorrow's forecast
- `weather --hourly` - Hourly forecast timeline
- `weather --format visual` - ASCII art weather display
- `weather --date "MMDDYYYY"` - Historical or forecast data
- Auto-detection of current location
- Metric and imperial unit support
- Configurable caching and timeout settings

[1.0.0]: https://github.com/mikebc23/weather-cli/releases/tag/v1.0.0
