#!/bin/bash
# Build and publish to PyPI

set -e

echo "🏗️  Building weather-cli for PyPI..."

# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Install build dependencies
pip install --upgrade build twine

# Build the package
python -m build

# Check the distribution
twine check dist/*

echo "✅ Build complete!"
echo ""
echo "📋 Next steps:"
echo "1. Test the package: pip install dist/weather_cli-*.whl"
echo "2. Upload to TestPyPI: twine upload --repository testpypi dist/*"
echo "3. Test install: pip install --index-url https://test.pypi.org/simple/ weather-cli"
echo "4. Upload to PyPI: twine upload dist/*"
echo ""
echo "🚀 After publishing, users can install with:"
echo "   pip install cr-mb-weather-cli"
