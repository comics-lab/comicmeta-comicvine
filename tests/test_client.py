"""
Tests for ComicVine API client.
"""
import pytest
from unittest.mock import patch, MagicMock

from comicmeta_comicvine.client import (
    ComicVineClient,
    ComicVineError,
    APIError,
    RateLimitError,
)

@pytest.fixture
def mock_response():
    """Create a mock response with test data."""
    return {
        "error": "OK",
        "limit": 100,
        "offset": 0,
        "number_of_page_results": 1,
        "number_of_total_results": 1,
        "results": [{
            "id": 123,
            "name": "Test Volume",
            "publisher": {"id": 31, "name": "Marvel"},
            "start_year": 2023,
        }]
    }

@pytest.fixture
def client():
    """Create a client instance with dummy API key."""
    return ComicVineClient(api_key="test_key")

def test_search_volumes_basic(client, mock_response):
    """Test basic volume search functionality."""
    with patch("comicmeta_comicvine.client._rate_limited_get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        
        results = client.search_volumes("Spider-Man")
        
        # Verify request parameters
        mock_get.assert_called_once()
        call_args = mock_get.call_args[0][1]
        assert call_args["query"] == "Spider-Man"
        assert call_args["resources"] == "volume"
        assert call_args["api_key"] == "test_key"

def test_search_volumes_with_publisher(client, mock_response):
    """Test volume search with publisher filter."""
    with patch("comicmeta_comicvine.client._rate_limited_get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        
        results = client.search_volumes("Spider-Man", publisher="Marvel Comics")
        
        call_args = mock_get.call_args[0][1]
        assert "filter" in call_args
        assert "publisher:" in call_args["filter"]

def test_get_volume(client, mock_response):
    """Test retrieving specific volume."""
    with patch("comicmeta_comicvine.client._rate_limited_get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        
        volume_id = "12345"
        results = client.get_volume(volume_id)
        
        # Verify endpoint construction
        called_url = mock_get.call_args[0][0]
        assert volume_id in called_url

def test_api_error_handling(client):
    """Test handling of API error responses."""
    error_response = {
        "error": "Invalid API Key",
        "limit": 0,
        "offset": 0,
        "number_of_total_results": 0,
        "status_code": 100,
    }
    
    with patch("comicmeta_comicvine.client._rate_limited_get") as mock_get:
        mock_get.return_value.json.return_value = error_response
        
        with pytest.raises(APIError):
            client.search_volumes("Test")

def test_rate_limit_error(client):
    """Test handling of rate limit errors."""
    with patch("comicmeta_comicvine.client._rate_limited_get") as mock_get:
        mock_get.side_effect = RateLimitError("Rate limit exceeded")
        
        with pytest.raises(RateLimitError):
            client.search_volumes("Test")

def test_request_error(client):
    """Test handling of request errors."""
    with patch("comicmeta_comicvine.client._rate_limited_get") as mock_get:
        mock_get.side_effect = Exception("Network error")
        
        with pytest.raises(ComicVineError):
            client.search_volumes("Test")