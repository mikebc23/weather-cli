#!/bin/bash
# Get SHA256 hash for Homebrew formula

# Download the package from PyPI
curl -L -o cr-mb-weather-cli-1.0.0.tar.gz \
  "https://files.pythonhosted.org/packages/source/c/cr-mb-weather-cli/cr_mb_weather_cli-1.0.0.tar.gz"

# Calculate SHA256
sha256sum cr-mb-weather-cli-1.0.0.tar.gz

# Clean up
rm cr-mb-weather-cli-1.0.0.tar.gz

echo ""
echo "Copy the hash above and update homebrew/weather-cli.rb"
