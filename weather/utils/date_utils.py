"""Date parsing and validation utilities."""

import re
from datetime import datetime, timedelta
from typing import Optional, Tuple

from .exceptions import WeatherError


class DateParser:
    """Handles date parsing and validation for weather queries."""

    @staticmethod
    def parse_date_input(date_str: Optional[str]) -> Tuple[datetime, str]:
        """
        Parse date input and return datetime and query type.
        
        Args:
            date_str: Date string or None for today
            
        Returns:
            Tuple of (datetime_obj, query_type)
            query_type: 'current', 'historical', 'forecast'
            
        Raises:
            WeatherError: If date string is invalid
        """
        if date_str is None or date_str.lower() == "today":
            return datetime.now(), "current"
            
        if date_str.lower() == "tomorrow":
            tomorrow = datetime.now() + timedelta(days=1)
            return tomorrow, "forecast"
            
        # Parse MMDDYYYY format
        if re.match(r"^\d{8}$", date_str):
            return DateParser._parse_mmddyyyy(date_str)
            
        raise WeatherError(f"Invalid date format: {date_str}")

    @staticmethod
    def _parse_mmddyyyy(date_str: str) -> Tuple[datetime, str]:
        """Parse MMDDYYYY format date string."""
        try:
            month = int(date_str[:2])
            day = int(date_str[2:4])
            year = int(date_str[4:8])
            
            parsed_date = datetime(year, month, day)
            
            # Determine if historical or forecast
            today = datetime.now()
            if parsed_date.date() < today.date():
                query_type = "historical"
            elif parsed_date.date() > today.date():
                query_type = "forecast"
            else:
                query_type = "current"
                
            return parsed_date, query_type
            
        except ValueError as e:
            raise WeatherError(
                f"Invalid date: {date_str}. Use MMDDYYYY format"
            ) from e

    @staticmethod
    def format_date(date_obj: datetime) -> str:
        """Format datetime object for display or API calls."""
        return date_obj.strftime("%Y-%m-%d")

    # Alias format_date_for_api to format_date for semantic clarity
    format_date_for_api = format_date

    @staticmethod
    def validate_date_range(date_obj: datetime) -> None:
        """
        Validate that date is within supported range.
        
        Args:
            date_obj: Date to validate
            
        Raises:
            WeatherError: If date is outside supported range
        """
        today = datetime.now()
        
        # Check historical limit (2 years back)
        earliest_date = today - timedelta(days=730)
        if date_obj < earliest_date:
            raise WeatherError(
                f"Date too far in the past. "
                f"Earliest supported: {earliest_date.strftime('%Y-%m-%d')}"
            )
            
        # Check forecast limit (16 days ahead)
        latest_date = today + timedelta(days=16)
        if date_obj > latest_date:
            raise WeatherError(
                f"Date too far in the future. "
                f"Latest supported: {latest_date.strftime('%Y-%m-%d')}"
            )
