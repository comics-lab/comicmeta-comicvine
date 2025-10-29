"""
ComicVine API client with rate limiting and response validation.
"""
from typing import Optional, Dict, Any, List
import time
import logging
from urllib.parse import urljoin

import requests
from ratelimit import limits, sleep_and_retry

from .config import (
    API_BASE_URL,
    REQUIRED_PARAMS,
    ENDPOINTS,
    DEFAULT_FIELDS,
    DEFAULT_RATE_LIMIT,
    VALIDATION_FIELDS,
)
from .auth import ensure_api_key
from .publishers import get_publisher_id, normalize_publisher

logger = logging.getLogger(__name__)

class ComicVineError(Exception):
    """Base exception for ComicVine API errors."""
    pass

class RateLimitError(ComicVineError):
    """Raised when rate limit is exceeded."""
    pass

class APIError(ComicVineError):
    """Raised when API returns an error response."""
    pass

@sleep_and_retry
@limits(calls=1, period=DEFAULT_RATE_LIMIT)
def _rate_limited_get(url: str, params: Dict[str, Any]) -> requests.Response:
    """Make a rate-limited GET request to the ComicVine API."""
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response

class ComicVineClient:
    """
    Client for the ComicVine API with rate limiting and response validation.
    
    Usage:
        client = ComicVineClient()
        results = client.search_volumes(
            query="Amazing Spider-Man",
            publisher="Marvel Comics"
        )
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize client with optional API key (otherwise loads from config)."""
        self.api_key = api_key or ensure_api_key()
        self.session = requests.Session()
    
    def _get(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make a GET request to the API with proper parameters and validation."""
        url = urljoin(API_BASE_URL, endpoint)
        
        # Merge required params
        request_params = REQUIRED_PARAMS.copy()
        request_params["api_key"] = self.api_key
        request_params.update(params)
        
        try:
            response = _rate_limited_get(url, request_params)
            data = response.json()
        except requests.exceptions.RequestException as e:
            raise ComicVineError(f"Request failed: {e}")
        except ValueError as e:
            raise ComicVineError(f"Invalid JSON response: {e}")
        
        # Validate response
        if data.get("error", "OK") != "OK":
            raise APIError(f"API error: {data.get('error', 'Unknown error')}")
        
        return data
    
    def search_volumes(
        self,
        query: str,
        publisher: Optional[str] = None,
        year: Optional[int] = None,
        fields: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Search for comic volumes/series.
        
        Args:
            query: Search term (e.g., "Spider-Man")
            publisher: Publisher name to filter by (e.g., "Marvel Comics")
            year: Filter by start year
            fields: List of fields to return (defaults to DEFAULT_FIELDS["volume"])
        
        Returns:
            Dict containing search results and metadata
        """
        params = {
            "query": query,
            "resources": "volume",
            "field_list": ",".join(fields or DEFAULT_FIELDS["volume"]),
        }
        
        # Add publisher filter if specified
        if publisher:
            publisher_id = get_publisher_id(publisher)
            if not publisher_id:
                raise ValueError(f"Unknown publisher: {publisher}")
            params["filter"] = f"publisher:{publisher_id}"
        
        # Add year filter
        if year:
            year_filter = f"start_year:{year}"
            params["filter"] = year_filter if "filter" not in params else f"{params['filter']},{year_filter}"
        
        return self._get(ENDPOINTS["search"], params)
    
    def get_volume(self, volume_id: str, fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """Get detailed information about a specific volume/series."""
        params = {
            "field_list": ",".join(fields or DEFAULT_FIELDS["volume"])
        }
        endpoint = ENDPOINTS["volume"].format(volume_id=volume_id)
        return self._get(endpoint, params)
    
    def get_publisher(self, publisher_id: int, fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """Get detailed information about a publisher."""
        params = {
            "field_list": ",".join(fields or DEFAULT_FIELDS["publisher"])
        }
        endpoint = ENDPOINTS["publisher"].format(publisher_id=publisher_id)
        return self._get(endpoint, params)