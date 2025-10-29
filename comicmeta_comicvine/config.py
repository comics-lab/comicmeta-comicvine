"""
ComicVine API configuration and constants.
"""

# Base URL for ComicVine API
API_BASE_URL = "https://comicvine.gamespot.com/api"

# Required query parameters for all API requests
REQUIRED_PARAMS = {
    "format": "json",
    "api_key": None,  # Must be set at runtime
}

# API endpoints
ENDPOINTS = {
    "publisher": "/publisher/4010-{publisher_id}",
    "volume": "/volume/4050-{volume_id}",
    "issue": "/issue/4000-{issue_id}",
    "search": "/search",
    "volumes": "/volumes",
}

# Fields always included in responses for validation
VALIDATION_FIELDS = [
    "error",
    "status_code",
    "number_of_total_results",
    "number_of_page_results",
]

# Default fields to retrieve
DEFAULT_FIELDS = {
    "publisher": [
        "id",
        "name",
        "description",
        "image",
        "deck",
        "api_detail_url",
    ],
    "volume": [
        "id",
        "name",
        "description",
        "start_year",
        "publisher",
        "count_of_issues",
        "image",
        "api_detail_url",
    ],
    "issue": [
        "id",
        "name",
        "issue_number",
        "volume",
        "image",
        "cover_date",
        "description",
        "api_detail_url",
    ],
}

# Rate limiting settings (in seconds)
DEFAULT_RATE_LIMIT = 1.0  # 1 request per second by default
BATCH_RATE_LIMIT = 0.5    # 2 requests per second for batch operations

# Cache settings
DEFAULT_CACHE_TTL = 86400  # 24 hours
PUBLISHER_CACHE_TTL = 604800  # 7 days - publishers change rarely