#!/bin/bash
# Setup script for weather-cli development environment

set -e

echo "🚀 Setting up weather-cli development environment..."

# Install development dependencies
echo "📦 Installing development dependencies..."
pip install -r requirements-dev.txt

# Install pre-commit hooks
echo "🔗 Installing pre-commit hooks..."
pre-commit install

echo "✅ Development environment setup complete!"

echo ""
echo "Next steps:"
echo "1. Run 'pre-commit run --all-files' to check and fix code issues"
echo "2. Run 'pytest' to run tests"
echo "3. Run 'pre-commit autoupdate' to update hook versions"

echo ""
echo "Available linters and tools:"
echo "• Black - Code formatting"
echo "• isort - Import sorting"
echo "• flake8 - Linting (with extensions for docstrings, imports, and bugs)"
echo "• mypy - Static type checking"
echo "• bandit - Security linting"
echo "• pydocstyle - Docstring style checking"
echo "• pyupgrade - Python syntax upgrading"
echo "• autoflake - Remove unused imports and variables"
echo "• markdownlint - Markdown linting"
echo "• prettier - YAML formatting"
