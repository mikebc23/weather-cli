"""Caching system for weather data to reduce API calls."""

import json
import time
import hashlib
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime, timezone

from .utils.exceptions import CacheError


class WeatherCache:
    """Simple file-based cache for weather data."""
    
    def __init__(self, cache_dir: Optional[str] = None, cache_duration: int = 300):
        """
        Initialize cache system.
        
        Args:
            cache_dir: Directory for cache files (default: ~/.weather_cache)
            cache_duration: Cache duration in seconds (default: 5 minutes)
        """
        self.cache_duration = cache_duration
        
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            self.cache_dir = Path.home() / '.weather_cache'
        
        # Create cache directory if it doesn't exist
        try:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise CacheError(f"Failed to create cache directory: {e}") from e
    
    def _get_cache_key(self, location: str, source: str, units: str) -> str:
        """
        Generate cache key for the given parameters.
        
        Args:
            location: Location identifier (coordinates, city name, etc.)
            source: Weather data source name
            units: Unit system (metric/imperial)
            
        Returns:
            MD5 hash as cache key
        """
        key_data = f"{location}:{source}:{units}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _get_cache_file(self, cache_key: str) -> Path:
        """Get cache file path for the given key."""
        return self.cache_dir / f"{cache_key}.json"
    
    def get(self, location: str, source: str, units: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached weather data.
        
        Args:
            location: Location identifier
            source: Weather data source name
            units: Unit system
            
        Returns:
            Cached data if valid, None otherwise
        """
        try:
            cache_key = self._get_cache_key(location, source, units)
            cache_file = self._get_cache_file(cache_key)
            
            if not cache_file.exists():
                return None
            
            # Read cache file
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # Check if cache is still valid
            cached_time = cache_data.get('cached_at', 0)
            current_time = time.time()
            
            if current_time - cached_time > self.cache_duration:
                # Cache expired, remove file
                cache_file.unlink(missing_ok=True)
                return None
            
            # Mark as cache hit
            weather_data = cache_data.get('data', {})
            weather_data['cache_hit'] = True
            weather_data['cached_at'] = datetime.fromtimestamp(
                cached_time, tz=timezone.utc
            ).isoformat()
            
            return weather_data
            
        except (json.JSONDecodeError, KeyError, OSError):
            # If there's any error reading cache, just return None
            return None
    
    def set(self, location: str, source: str, units: str, data: Dict[str, Any]) -> None:
        """
        Cache weather data.
        
        Args:
            location: Location identifier
            source: Weather data source name
            units: Unit system
            data: Weather data to cache
        """
        try:
            cache_key = self._get_cache_key(location, source, units)
            cache_file = self._get_cache_file(cache_key)
            
            # Prepare cache data
            cache_data = {
                'cached_at': time.time(),
                'location': location,
                'source': source,
                'units': units,
                'data': data
            }
            
            # Write to cache file
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
                
        except OSError:
            # Don't fail if caching fails, just log and continue
            pass
    
    def clear(self) -> None:
        """Clear all cached data."""
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink(missing_ok=True)
        except OSError:
            pass
    
    def cleanup_expired(self) -> int:
        """
        Remove expired cache files.
        
        Returns:
            Number of files removed
        """
        removed_count = 0
        current_time = time.time()
        
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                try:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        cache_data = json.load(f)
                    
                    cached_time = cache_data.get('cached_at', 0)
                    if current_time - cached_time > self.cache_duration:
                        cache_file.unlink(missing_ok=True)
                        removed_count += 1
                        
                except (json.JSONDecodeError, KeyError, OSError):
                    # Remove corrupted cache files
                    cache_file.unlink(missing_ok=True)
                    removed_count += 1
                    
        except OSError:
            pass
        
        return removed_count
    
    def get_cache_info(self) -> Dict[str, Any]:
        """
        Get information about the cache.
        
        Returns:
            Dictionary with cache statistics
        """
        try:
            cache_files = list(self.cache_dir.glob("*.json"))
            valid_files = 0
            expired_files = 0
            corrupted_files = 0
            current_time = time.time()
            
            for cache_file in cache_files:
                try:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        cache_data = json.load(f)
                    
                    cached_time = cache_data.get('cached_at', 0)
                    if current_time - cached_time > self.cache_duration:
                        expired_files += 1
                    else:
                        valid_files += 1
                        
                except (json.JSONDecodeError, KeyError):
                    corrupted_files += 1
            
            return {
                'cache_dir': str(self.cache_dir),
                'total_files': len(cache_files),
                'valid_files': valid_files,
                'expired_files': expired_files,
                'corrupted_files': corrupted_files,
                'cache_duration': self.cache_duration
            }
            
        except OSError:
            return {
                'cache_dir': str(self.cache_dir),
                'total_files': 0,
                'valid_files': 0,
                'expired_files': 0,
                'corrupted_files': 0,
                'cache_duration': self.cache_duration
            }
