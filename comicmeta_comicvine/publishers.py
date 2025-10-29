"""
ComicVine publisher mapping and validation.
"""
from typing import Dict, Optional

# Map common publisher names/aliases to ComicVine publisher IDs
PUBLISHER_MAP: Dict[str, int] = {
    # Major publishers
    "marvel": 31,           # Marvel Comics
    "dc": 10,              # DC Comics
    "image": 4,            # Image
    "dark horse": 3,       # Dark Horse Comics
    
    # Aliases/variations
    "marvel comics": 31,
    "dc comics": 10,
    "dc entertainment": 10,
    "image comics": 4,
    "dark horse comics": 3,
    
    # Imprints
    "vertigo": 10,         # DC imprint
    "max": 31,             # Marvel MAX imprint
    "icon": 31,            # Marvel Icon imprint
    "wildstorm": 10,       # DC WildStorm imprint
}

def normalize_publisher(name: str) -> str:
    """Convert publisher name to normalized form (lowercase, stripped)."""
    return name.lower().strip()

def get_publisher_id(name: str) -> Optional[int]:
    """
    Get ComicVine publisher ID from name.
    Returns None if publisher not found.
    """
    normalized = normalize_publisher(name)
    return PUBLISHER_MAP.get(normalized)

def is_valid_publisher(name: str) -> bool:
    """Check if a publisher name is valid/known."""
    return get_publisher_id(name) is not None

def get_known_publishers() -> list[str]:
    """Get list of known publisher names (primary names only)."""
    return sorted(set([
        "Marvel Comics",
        "DC Comics", 
        "Image Comics",
        "Dark Horse Comics"
    ]))