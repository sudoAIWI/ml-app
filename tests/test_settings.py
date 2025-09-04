import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from settings import Settings
from dotenv import load_dotenv


def test_settings_loading():
    """Test that settings are loaded correctly from environment"""
    load_dotenv(".env.test", override=True)

    # Load secrets manually for testing
    Settings.load_secrets()

    settings = Settings()

    assert settings.ENVIRONMENT == "test"
    assert settings.APP_NAME == "ML App Test"


def test_environment_validation():
    """Test environment validation - valid case"""
    original_env = os.environ.get("ENVIRONMENT")
    os.environ["ENVIRONMENT"] = "dev"
    settings = Settings()
    assert settings.ENVIRONMENT == "dev"
    _restore_environment(original_env)


def test_environment_validation_invalid():
    """Test environment validation - invalid case"""
    original_env = os.environ.get("ENVIRONMENT")
    os.environ["ENVIRONMENT"] = "invalid"
    try:
        Settings()
        assert False, "Should have raised ValidationError"
    except ValueError as e:
        assert "Environment must be one of" in str(e)
    _restore_environment(original_env)


def _restore_environment(original_env):
    """Helper to restore environment"""
    if original_env:
        os.environ["ENVIRONMENT"] = original_env
    elif "ENVIRONMENT" in os.environ:
        del os.environ["ENVIRONMENT"]
