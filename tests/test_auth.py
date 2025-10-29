import os
import pytest
from unittest.mock import patch
from pathlib import Path
from comicmeta_comicvine.auth import get_api_key, ensure_api_key

def test_get_api_key_from_env():
    with patch.dict(os.environ, {"COMICVINE_API_KEY": "test-key-123"}):
        assert get_api_key() == "test-key-123"

def test_get_api_key_from_config_file(tmp_path):
    config_dir = tmp_path / ".config" / "comicvine"
    config_dir.mkdir(parents=True)
    config_file = config_dir / "api_key"
    config_file.write_text("test-key-456")
    
    with patch("pathlib.Path.home", return_value=tmp_path):
        assert get_api_key() == "test-key-456"

def test_get_api_key_from_env_file(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text('COMICVINE_API_KEY="test-key-789"')
    
    with patch("pathlib.Path.cwd", return_value=tmp_path):
        assert get_api_key() == "test-key-789"

def test_ensure_api_key_missing():
    with patch("comicmeta_comicvine.auth.get_api_key", return_value=None):
        with pytest.raises(RuntimeError) as exc:
            ensure_api_key()
        assert "ComicVine API key not found" in str(exc.value)