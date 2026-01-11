import logging
from datetime import datetime, timedelta
from typing import Optional, List

from ..api.weather_client import OpenMeteoClient, WeatherAPIError
from ..api.geocoding_client import GeocodingClient, GeocodingError
from ..api.geolocation_client import GeolocationClient, GeolocationError
from ..models.weather_data import CompleteWeatherData
from ..models.location import Location
from ..models.settings import Settings
from .settings_service import SettingsService

logger = logging.getLogger(__name__)


class WeatherService:
    """Orchestrates weather data fetching with caching."""

    CACHE_DURATION_MINUTES = 5  # Cache weather data for 5 minutes

    def __init__(self, settings_service: SettingsService):
        self.settings_service = settings_service
        self.weather_client = OpenMeteoClient()
        self.geocoding_client = GeocodingClient()
        self.geolocation_client = GeolocationClient()
        self._cache: Optional[CompleteWeatherData] = None
        self._cache_timestamp: Optional[datetime] = None
        self._cache_location: Optional[Location] = None

    def get_weather(self, force_refresh: bool = False) -> CompleteWeatherData:
        """
        Get weather data for current location.

        Uses cached data if available and fresh, otherwise fetches new data.

        Args:
            force_refresh: If True, bypass cache and fetch fresh data

        Returns:
            CompleteWeatherData with current weather and forecasts

        Raises:
            WeatherServiceError: If weather data cannot be fetched
        """
        settings = self.settings_service.load()
        location = self._get_location(settings)

        # Check cache validity
        if not force_refresh and self._is_cache_valid(location):
            logger.debug("Using cached weather data")
            return self._cache

        try:
            logger.info(f"Fetching weather for {location.display_name}")
            weather = self.weather_client.get_complete_weather(
                latitude=location.latitude,
                longitude=location.longitude,
                use_fahrenheit=settings.use_fahrenheit,
                location_name=location.display_name
            )

            # Update cache
            self._cache = weather
            self._cache_timestamp = datetime.now()
            self._cache_location = location

            return weather

        except WeatherAPIError as e:
            logger.error(f"Failed to fetch weather: {e}")
            # Return cached data if available
            if self._cache is not None:
                logger.warning("Returning stale cached data due to API error")
                return self._cache
            raise WeatherServiceError(f"Failed to fetch weather: {e}") from e

    def _get_location(self, settings: Settings) -> Location:
        """Get current location based on settings."""
        if settings.location_mode == "manual" and settings.location:
            return settings.location

        # Auto-detect mode or no saved location
        if settings.location_mode == "auto":
            try:
                location = self.geolocation_client.detect_location()
                # Save detected location
                self.settings_service.update(location=location)
                return location
            except GeolocationError as e:
                logger.warning(f"Auto-detect failed: {e}")

        # Fallback to saved location or default
        if settings.location:
            return settings.location

        return Location.default()

    def _is_cache_valid(self, location: Location) -> bool:
        """Check if cached data is still valid."""
        if self._cache is None or self._cache_timestamp is None:
            return False

        # Check if cache is for same location
        if self._cache_location is None:
            return False

        if (self._cache_location.latitude != location.latitude or
            self._cache_location.longitude != location.longitude):
            return False

        # Check if cache is fresh
        age = datetime.now() - self._cache_timestamp
        return age < timedelta(minutes=self.CACHE_DURATION_MINUTES)

    def search_locations(self, query: str) -> List[Location]:
        """
        Search for locations by name.

        Args:
            query: Location name to search for

        Returns:
            List of matching Location objects
        """
        try:
            return self.geocoding_client.search(query)
        except GeocodingError as e:
            logger.error(f"Location search failed: {e}")
            return []

    def set_location(self, location: Location) -> None:
        """
        Set manual location.

        Args:
            location: Location to set
        """
        self.settings_service.update(
            location=location,
            location_mode="manual"
        )
        # Invalidate cache since location changed
        self._cache = None
        self._cache_timestamp = None

    def auto_detect_location(self) -> Location:
        """
        Auto-detect location from IP address.

        Returns:
            Detected Location

        Raises:
            WeatherServiceError: If detection fails
        """
        try:
            location = self.geolocation_client.detect_location()
            self.settings_service.update(
                location=location,
                location_mode="auto"
            )
            # Invalidate cache
            self._cache = None
            self._cache_timestamp = None
            return location
        except GeolocationError as e:
            raise WeatherServiceError(f"Failed to detect location: {e}") from e

    def get_cached_data(self) -> Optional[CompleteWeatherData]:
        """Get cached weather data without fetching."""
        return self._cache


class WeatherServiceError(Exception):
    """Exception raised when weather service operations fail."""
    pass
