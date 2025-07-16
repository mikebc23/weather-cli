"""Setup configuration for weather-cli package."""

from pathlib import Path

from setuptools import find_packages, setup

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = (
    readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""
)

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = requirements_file.read_text(encoding="utf-8").strip().split("\n")
    requirements = [
        req.strip() for req in requirements if req.strip() and not req.startswith("#")
    ]

setup(
    name="weather-cli",
    version="1.0.0",
    author="Mike",
    author_email="mike@example.com",
    description="A simple command-line weather tool with multiple data sources and output formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mikebc23/weather-cli",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "weather=weather.main:main",
        ],
    },
    keywords="weather cli command-line forecast meteorology",
    project_urls={
        "Bug Reports": "https://github.com/mikebc23/weather-cli/issues",
        "Source": "https://github.com/mikebc23/weather-cli",
    },
)
