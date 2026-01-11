import requests
import logging
from typing import List

from ..models.location import Location

logger = logging.getLogger(__name__)


class GeocodingClient:
    """Client for Open-Meteo Geocoding API."""

    BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"
    TIMEOUT = 10

    def search(self, query: str, count: int = 5) -> List[Location]:
        """
        Search for locations by name.

        Args:
            query: Location name to search for
            count: Maximum number of results to return

        Returns:
            List of Location objects matching the query
        """
        if not query or not query.strip():
            return []

        params = {
            "name": query.strip(),
            "count": count,
            "language": "en",
            "format": "json"
        }

        try:
            logger.info(f"Searching for location: {query}")
            response = requests.get(self.BASE_URL, params=params, timeout=self.TIMEOUT)
            response.raise_for_status()
            data = response.json()

            results = data.get('results', [])
            locations = []

            for result in results:
                locations.append(Location(
                    name=result.get('name', ''),
                    latitude=result.get('latitude', 0),
                    longitude=result.get('longitude', 0),
                    country=result.get('country', ''),
                    timezone=result.get('timezone', 'UTC'),
                    country_code=result.get('country_code'),
                    admin1=result.get('admin1')
                ))

            return locations

        except requests.RequestException as e:
            logger.error(f"Failed to search location: {e}")
            raise GeocodingError(f"Failed to search location: {e}") from e


class GeocodingError(Exception):
    """Exception raised when geocoding API call fails."""
    pass
