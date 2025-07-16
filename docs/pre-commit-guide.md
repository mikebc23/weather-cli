# Pre-commit Setup Guide

This document explains the pre-commit configuration for the weather-cli project and how to use the various linters and code quality tools.

## Overview

Pre-commit is configured to run automatically before each git commit to ensure code quality and consistency. The configuration includes:

### Code Formatting
- **Black**: Opinionated Python code formatter
- **isort**: Import statement organizer
- **Prettier**: YAML file formatter

### Code Quality & Linting
- **flake8**: Python linting with extensions:
  - `flake8-docstrings`: Docstring conventions
  - `flake8-import-order`: Import order checking
  - `flake8-bugbear`: Additional bug and design problems
- **autoflake**: Removes unused imports and variables
- **pyupgrade**: Upgrades Python syntax for newer versions

### Type Checking
- **mypy**: Static type checker for Python

### Security
- **bandit**: Security vulnerability scanner

### Documentation
- **pydocstyle**: Docstring style checker (Google convention)
- **markdownlint**: Markdown file linter

### File Maintenance
- Trailing whitespace removal
- End-of-file fixing
- Large file checking
- Merge conflict detection
- Debug statement detection

## Setup

### Initial Setup
```bash
# Install pre-commit and development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Or use the setup script
./setup-dev.sh
```

### Manual Installation
```bash
pip install pre-commit
pre-commit install
```

## Usage

### Automatic Usage
Pre-commit hooks run automatically on `git commit`. If any hook fails:
1. The commit is blocked
2. Issues are automatically fixed where possible
3. You need to stage the fixes and commit again

### Manual Usage
```bash
# Run all hooks on all files
pre-commit run --all-files

# Run specific hook
pre-commit run black
pre-commit run flake8
pre-commit run mypy

# Run hooks on specific files
pre-commit run --files weather/location.py

# Skip hooks for a commit (not recommended)
git commit --no-verify
```

## Configuration Files

### `.pre-commit-config.yaml`
Main configuration file defining all hooks and their settings.

### `pyproject.toml`
Contains tool-specific configurations:
- Black formatting options
- isort import organization
- mypy type checking settings
- bandit security scanning
- pytest and coverage settings

### `.markdownlint.yaml`
Markdown linting rules configuration.

## Tool-Specific Information

### Black
- Line length: 88 characters
- Target Python version: 3.8+
- Automatically formats code on commit

### isort
- Profile: black (compatible with Black)
- Sorts imports by: standard library, third-party, local
- Groups imports with trailing commas

### flake8
- Max line length: 88 (Black compatible)
- Max complexity: 10
- Ignores: E203, W503, E501 (Black compatibility)

### mypy
- Configured for gradual typing adoption
- Initially lenient, can be made stricter over time
- Ignores missing imports for third-party libraries

### bandit
- Scans for security vulnerabilities
- Excludes test files
- Custom configuration for acceptable patterns

### pydocstyle
- Google docstring convention
- Some rules disabled for gradual adoption

## Common Issues and Solutions

### Type Errors
```bash
# For Python 3.8 compatibility, use typing imports
from typing import List, Dict, Tuple
# Instead of: list, dict, tuple
```

### Import Order
isort will automatically fix import order issues.

### Line Length
Black automatically handles line length, but some cases may need manual adjustment.

### Docstring Issues
Follow Google docstring convention:
```python
def function(param: str) -> str:
    """Brief description.
    
    Args:
        param: Description of parameter.
        
    Returns:
        Description of return value.
    """
```

### Security Issues
- Use `# nosec` comment for false positives
- Address real security issues promptly

## Updating Hooks

```bash
# Update all hooks to latest versions
pre-commit autoupdate

# Update specific hook
pre-commit autoupdate --repo https://github.com/psf/black
```

## Disabling Hooks

To temporarily disable a hook, edit `.pre-commit-config.yaml` and add:
```yaml
- repo: local
  hooks:
    - id: disabled-hook
      name: disabled hook
      entry: /bin/true
      language: system
```

Or use `SKIP` environment variable:
```bash
SKIP=mypy git commit -m "Skip mypy for this commit"
```

## IDE Integration

### VS Code
Install these extensions for better integration:
- Python
- Black Formatter
- isort
- Pylance (for mypy-like checking)
- markdownlint

### PyCharm
Enable these features:
- Code reformatting with Black
- Import optimization with isort
- Type checking with mypy
- Security scanning with bandit

## Gradual Adoption

The configuration is initially lenient to allow gradual adoption. You can make it stricter over time by:

1. Reducing mypy `--allow-*` flags
2. Enabling more pydocstyle rules
3. Lowering flake8 complexity limits
4. Adding more bandit security checks

## Troubleshooting

### Pre-commit not running
```bash
# Reinstall hooks
pre-commit uninstall
pre-commit install
```

### Hook failures
```bash
# See detailed output
pre-commit run --verbose --all-files

# Debug specific hook
pre-commit run --verbose flake8
```

### Performance issues
```bash
# Run hooks in parallel (default)
pre-commit run --show-diff-on-failure

# Skip slow hooks during development
SKIP=mypy,bandit git commit -m "Quick fix"
```
