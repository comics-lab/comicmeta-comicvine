import pytest
from comicmeta_comicvine.publishers import (
    get_publisher_id,
    is_valid_publisher,
    normalize_publisher,
    get_known_publishers
)

def test_normalize_publisher():
    assert normalize_publisher("Marvel Comics") == "marvel comics"
    assert normalize_publisher("DC  Comics  ") == "dc comics"
    assert normalize_publisher("MARVEL") == "marvel"

def test_get_publisher_id():
    assert get_publisher_id("Marvel Comics") == 31
    assert get_publisher_id("marvel") == 31
    assert get_publisher_id("DC") == 10
    assert get_publisher_id("Unknown Publisher") is None

def test_is_valid_publisher():
    assert is_valid_publisher("Marvel Comics") is True
    assert is_valid_publisher("DC Comics") is True
    assert is_valid_publisher("Unknown Publisher") is False

def test_get_known_publishers():
    publishers = get_known_publishers()
    assert "Marvel Comics" in publishers
    assert "DC Comics" in publishers
    assert len(publishers) >= 4  # At least the major publishers