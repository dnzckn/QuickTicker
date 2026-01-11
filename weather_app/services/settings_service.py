import json
import logging
from pathlib import Path
from typing import Optional

from ..models.settings import Settings

logger = logging.getLogger(__name__)


class SettingsService:
    """Manages loading and saving user settings."""

    # Standard macOS application support directory
    SETTINGS_DIR = Path.home() / "Library" / "Application Support" / "WeatherBar"
    SETTINGS_FILE = SETTINGS_DIR / "settings.json"

    def __init__(self):
        self._settings: Optional[Settings] = None
        self._ensure_settings_dir()

    def _ensure_settings_dir(self):
        """Create settings directory if it doesn't exist."""
        try:
            self.SETTINGS_DIR.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            logger.error(f"Failed to create settings directory: {e}")

    def load(self) -> Settings:
        """
        Load settings from file.

        Returns default settings if file doesn't exist or is invalid.
        """
        if self._settings is not None:
            return self._settings

        if not self.SETTINGS_FILE.exists():
            logger.info("No settings file found, using defaults")
            self._settings = Settings.default()
            return self._settings

        try:
            with open(self.SETTINGS_FILE, 'r') as f:
                data = json.load(f)
                self._settings = Settings.from_dict(data)
                logger.info("Settings loaded successfully")
                return self._settings

        except (json.JSONDecodeError, KeyError, TypeError) as e:
            logger.warning(f"Failed to parse settings file, using defaults: {e}")
            self._settings = Settings.default()
            return self._settings

        except OSError as e:
            logger.error(f"Failed to read settings file: {e}")
            self._settings = Settings.default()
            return self._settings

    def save(self, settings: Settings) -> bool:
        """
        Save settings to file.

        Args:
            settings: Settings object to save

        Returns:
            True if save succeeded, False otherwise
        """
        try:
            self._ensure_settings_dir()
            with open(self.SETTINGS_FILE, 'w') as f:
                json.dump(settings.to_dict(), f, indent=2)
            self._settings = settings
            logger.info("Settings saved successfully")
            return True

        except OSError as e:
            logger.error(f"Failed to save settings: {e}")
            return False

    def update(self, **kwargs) -> Settings:
        """
        Update specific settings values and save.

        Args:
            **kwargs: Setting names and values to update

        Returns:
            Updated Settings object
        """
        settings = self.load()

        for key, value in kwargs.items():
            if hasattr(settings, key):
                setattr(settings, key, value)
            else:
                logger.warning(f"Unknown setting: {key}")

        self.save(settings)
        return settings

    def reset(self) -> Settings:
        """Reset settings to defaults."""
        self._settings = Settings.default()
        self.save(self._settings)
        return self._settings
