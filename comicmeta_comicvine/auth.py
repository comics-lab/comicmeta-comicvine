"""
Configuration handling for ComicVine API.
"""
import os
from pathlib import Path
from typing import Optional

def get_api_key() -> Optional[str]:
    """
    Get ComicVine API key from environment or config file.
    Priority:
    1. COMICVINE_API_KEY environment variable
    2. ~/.config/comicvine/api_key file
    3. .env file in current directory
    """
    # Try environment variable
    api_key = os.getenv("COMICVINE_API_KEY")
    if api_key:
        return api_key

    # Try config file
    config_file = Path.home() / ".config" / "comicvine" / "api_key"
    if config_file.exists():
        return config_file.read_text().strip()

    # Try .env file
    env_file = Path(".env")
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("COMICVINE_API_KEY="):
                return line.split("=", 1)[1].strip().strip("'").strip('"')

    return None

def ensure_api_key() -> str:
    """Get API key or raise informative error."""
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError(
            "ComicVine API key not found. Please either:\n"
            "1. Set COMICVINE_API_KEY environment variable\n"
            "2. Create ~/.config/comicvine/api_key file\n"
            "3. Add COMICVINE_API_KEY to .env file\n\n"
            "Get your API key at: https://comicvine.gamespot.com/api/"
        )
    return api_key