import requests
import logging

from ..models.location import Location

logger = logging.getLogger(__name__)


class GeolocationClient:
    """Client for IP-based geolocation using ip-api.com."""

    BASE_URL = "http://ip-api.com/json/"
    TIMEOUT = 10

    def detect_location(self) -> Location:
        """
        Detect current location based on IP address.

        Returns:
            Location object for detected location

        Raises:
            GeolocationError: If location detection fails
        """
        try:
            logger.info("Detecting location from IP address")
            response = requests.get(self.BASE_URL, timeout=self.TIMEOUT)
            response.raise_for_status()
            data = response.json()

            if data.get('status') != 'success':
                raise GeolocationError(f"IP geolocation failed: {data.get('message', 'Unknown error')}")

            # Map state abbreviations for US locations
            admin1 = data.get('regionName', '')
            if data.get('countryCode') == 'US':
                admin1 = data.get('region', admin1)  # Use abbreviation for US states

            return Location(
                name=data.get('city', 'Unknown'),
                latitude=data.get('lat', 0),
                longitude=data.get('lon', 0),
                country=data.get('country', ''),
                timezone=data.get('timezone', 'UTC'),
                country_code=data.get('countryCode'),
                admin1=admin1
            )

        except requests.RequestException as e:
            logger.error(f"Failed to detect location: {e}")
            raise GeolocationError(f"Failed to detect location: {e}") from e


class GeolocationError(Exception):
    """Exception raised when geolocation fails."""
    pass
