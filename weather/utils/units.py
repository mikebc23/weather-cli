"""Unit conversion utilities for weather data."""


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9/5) + 32


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5/9


def kmh_to_mph(kmh: float) -> float:
    """Convert km/h to mph."""
    return kmh * 0.621371


def mph_to_kmh(mph: float) -> float:
    """Convert mph to km/h."""
    return mph * 1.60934


def hpa_to_inhg(hpa: float) -> float:
    """Convert hPa to inches of mercury."""
    return hpa * 0.02953


def inhg_to_hpa(inhg: float) -> float:
    """Convert inches of mercury to hPa."""
    return inhg * 33.8639


def mm_to_inch(mm: float) -> float:
    """Convert millimeters to inches."""
    return mm * 0.0393701


def inch_to_mm(inch: float) -> float:
    """Convert inches to millimeters."""
    return inch * 25.4


def m_to_ft(meters: float) -> float:
    """Convert meters to feet."""
    return meters * 3.28084


def ft_to_m(feet: float) -> float:
    """Convert feet to meters."""
    return feet * 0.3048


class UnitConverter:
    """Handles unit conversions for weather data."""
    
    def __init__(self, units: str = "metric"):
        """
        Initialize converter with unit system.
        
        Args:
            units: 'metric' or 'imperial'
        """
        self.units = units.lower()
        if self.units not in ['metric', 'imperial']:
            raise ValueError(f"Invalid units: {units}. Must be 'metric' or 'imperial'")
    
    def temperature(self, value: float, from_celsius: bool = True) -> tuple[float, str]:
        """
        Convert temperature to target units.
        
        Args:
            value: Temperature value
            from_celsius: True if input is Celsius, False if Fahrenheit
            
        Returns:
            Tuple of (converted_value, unit_symbol)
        """
        if self.units == "metric":
            if from_celsius:
                return value, "°C"
            else:
                return fahrenheit_to_celsius(value), "°C"
        else:  # imperial
            if from_celsius:
                return celsius_to_fahrenheit(value), "°F"
            else:
                return value, "°F"
    
    def wind_speed(self, value: float, from_kmh: bool = True) -> tuple[float, str]:
        """
        Convert wind speed to target units.
        
        Args:
            value: Wind speed value
            from_kmh: True if input is km/h, False if mph
            
        Returns:
            Tuple of (converted_value, unit_symbol)
        """
        if self.units == "metric":
            if from_kmh:
                return value, "km/h"
            else:
                return mph_to_kmh(value), "km/h"
        else:  # imperial
            if from_kmh:
                return kmh_to_mph(value), "mph"
            else:
                return value, "mph"
    
    def pressure(self, value: float, from_hpa: bool = True) -> tuple[float, str]:
        """
        Convert pressure to target units.
        
        Args:
            value: Pressure value
            from_hpa: True if input is hPa, False if inHg
            
        Returns:
            Tuple of (converted_value, unit_symbol)
        """
        if self.units == "metric":
            if from_hpa:
                return value, "hPa"
            else:
                return inhg_to_hpa(value), "hPa"
        else:  # imperial
            if from_hpa:
                return hpa_to_inhg(value), "inHg"
            else:
                return value, "inHg"
    
    def precipitation(self, value: float, from_mm: bool = True) -> tuple[float, str]:
        """
        Convert precipitation to target units.
        
        Args:
            value: Precipitation value
            from_mm: True if input is mm, False if inches
            
        Returns:
            Tuple of (converted_value, unit_symbol)
        """
        if self.units == "metric":
            if from_mm:
                return value, "mm"
            else:
                return inch_to_mm(value), "mm"
        else:  # imperial
            if from_mm:
                return mm_to_inch(value), "in"
            else:
                return value, "in"
    
    def visibility(self, value: float, from_meters: bool = True) -> tuple[float, str]:
        """
        Convert visibility to target units.
        
        Args:
            value: Visibility value
            from_meters: True if input is meters, False if feet
            
        Returns:
            Tuple of (converted_value, unit_symbol)
        """
        if self.units == "metric":
            if from_meters:
                return value / 1000, "km"  # Convert to km for readability
            else:
                return ft_to_m(value) / 1000, "km"
        else:  # imperial
            if from_meters:
                return m_to_ft(value), "ft"
            else:
                return value, "ft"


def format_temperature(temp: float, units: str) -> str:
    """Format temperature with appropriate units."""
    converter = UnitConverter(units)
    value, unit = converter.temperature(temp, from_celsius=True)
    return f"{value:.1f}{unit}"


def format_wind_speed(speed: float, units: str) -> str:
    """Format wind speed with appropriate units."""
    converter = UnitConverter(units)
    value, unit = converter.wind_speed(speed, from_kmh=True)
    return f"{value:.1f} {unit}"


def format_pressure(pressure: float, units: str) -> str:
    """Format pressure with appropriate units."""
    converter = UnitConverter(units)
    value, unit = converter.pressure(pressure, from_hpa=True)
    return f"{value:.1f} {unit}"
