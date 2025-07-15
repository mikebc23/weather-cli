"""HTTP client utilities with proper error handling and retry logic."""

import requests
from typing import Dict, Any, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .exceptions import NetworkError


class HTTPClient:
    """Enhanced HTTP client with retry logic and error handling."""
    
    def __init__(self, timeout: int = 10, retries: int = 3):
        """Initialize HTTP client with timeout and retry configuration."""
        self.timeout = timeout
        self.session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=retries,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"],
            backoff_factor=1  # Wait 1, 2, 4 seconds between retries
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Set default headers
        self.session.headers.update({
            'User-Agent': 'weather-cli/1.0.0 (https://github.com/user/weather-cli)',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate'
        })
    
    def get(self, url: str, params: Optional[Dict[str, Any]] = None, 
            headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Make GET request with error handling.
        
        Args:
            url: The URL to request
            params: Query parameters
            headers: Additional headers
            
        Returns:
            JSON response as dictionary
            
        Raises:
            NetworkError: If request fails
        """
        try:
            response = self.session.get(
                url, 
                params=params, 
                headers=headers, 
                timeout=self.timeout
            )
            response.raise_for_status()
            
            # Handle different content types
            content_type = response.headers.get('content-type', '').lower()
            
            if 'application/json' in content_type:
                return response.json()
            elif 'text/' in content_type:
                return {'text': response.text}
            else:
                return {'content': response.content.decode('utf-8', errors='ignore')}
                
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"HTTP request failed: {e}") from e
        except ValueError as e:
            raise NetworkError(f"Invalid JSON response: {e}") from e
    
    def close(self):
        """Close the HTTP session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
