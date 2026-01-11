import requests
import logging
from typing import List, Optional
from datetime import datetime

from ..models.weather_data import (
    CurrentWeather,
    HourlyForecast,
    DailyForecast,
    CompleteWeatherData
)

logger = logging.getLogger(__name__)


class OpenMeteoClient:
    """Client for Open-Meteo Weather API."""

    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    TIMEOUT = 10

    # Parameters for current weather
    CURRENT_PARAMS = [
        "temperature_2m",
        "relative_humidity_2m",
        "apparent_temperature",
        "weather_code",
        "wind_speed_10m",
        "wind_direction_10m",
        "pressure_msl",
        "visibility",
        "uv_index",
        "is_day"
    ]

    # Parameters for hourly forecast
    HOURLY_PARAMS = [
        "temperature_2m",
        "weather_code",
        "precipitation_probability"
    ]

    # Parameters for daily forecast
    DAILY_PARAMS = [
        "weather_code",
        "temperature_2m_max",
        "temperature_2m_min",
        "sunrise",
        "sunset",
        "precipitation_probability_max",
        "uv_index_max"
    ]

    def get_complete_weather(
        self,
        latitude: float,
        longitude: float,
        use_fahrenheit: bool = True,
        location_name: str = ""
    ) -> CompleteWeatherData:
        """
        Fetch complete weather data including current, hourly, and daily forecasts.

        Args:
            latitude: Location latitude
            longitude: Location longitude
            use_fahrenheit: If True, use Fahrenheit; otherwise Celsius
            location_name: Name of location for display

        Returns:
            CompleteWeatherData object with all weather information
        """
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": ",".join(self.CURRENT_PARAMS),
            "hourly": ",".join(self.HOURLY_PARAMS),
            "daily": ",".join(self.DAILY_PARAMS),
            "temperature_unit": "fahrenheit" if use_fahrenheit else "celsius",
            "wind_speed_unit": "mph" if use_fahrenheit else "kmh",
            "timezone": "auto",
            "forecast_days": 7
        }

        try:
            logger.info(f"Fetching weather for {latitude}, {longitude}")
            response = requests.get(self.BASE_URL, params=params, timeout=self.TIMEOUT)
            response.raise_for_status()
            data = response.json()

            current = CurrentWeather.from_api_response(data, data.get('current', {}))
            hourly = self._parse_hourly(data.get('hourly', {}))
            daily = self._parse_daily(data.get('daily', {}))

            return CompleteWeatherData(
                current=current,
                hourly=hourly,
                daily=daily,
                location_name=location_name
            )

        except requests.RequestException as e:
            logger.error(f"Failed to fetch weather data: {e}")
            raise WeatherAPIError(f"Failed to fetch weather: {e}") from e

    def _parse_hourly(self, hourly_data: dict) -> List[HourlyForecast]:
        """Parse hourly forecast data from API response."""
        forecasts = []
        times = hourly_data.get('time', [])
        temps = hourly_data.get('temperature_2m', [])
        codes = hourly_data.get('weather_code', [])
        precips = hourly_data.get('precipitation_probability', [])

        # Get next 24 hours starting from current hour
        now = datetime.now()
        for i, time_str in enumerate(times):
            if i >= len(temps):
                break
            forecast_time = datetime.fromisoformat(time_str)
            if forecast_time >= now:
                forecasts.append(HourlyForecast.from_api_data(
                    time_str=time_str,
                    temp=temps[i],
                    code=codes[i] if i < len(codes) else 0,
                    precip=precips[i] if i < len(precips) else 0
                ))
            if len(forecasts) >= 24:
                break

        return forecasts

    def _parse_daily(self, daily_data: dict) -> List[DailyForecast]:
        """Parse daily forecast data from API response."""
        forecasts = []
        dates = daily_data.get('time', [])
        temp_maxs = daily_data.get('temperature_2m_max', [])
        temp_mins = daily_data.get('temperature_2m_min', [])
        codes = daily_data.get('weather_code', [])
        precips = daily_data.get('precipitation_probability_max', [])
        uvs = daily_data.get('uv_index_max', [])
        sunrises = daily_data.get('sunrise', [])
        sunsets = daily_data.get('sunset', [])

        for i, date_str in enumerate(dates):
            if i >= len(temp_maxs) or i >= len(temp_mins):
                break
            forecasts.append(DailyForecast.from_api_data(
                date_str=date_str,
                temp_max=temp_maxs[i],
                temp_min=temp_mins[i],
                code=codes[i] if i < len(codes) else 0,
                precip=precips[i] if i < len(precips) else 0,
                uv=uvs[i] if i < len(uvs) else 0,
                sunrise_str=sunrises[i] if i < len(sunrises) else date_str + "T06:00",
                sunset_str=sunsets[i] if i < len(sunsets) else date_str + "T18:00"
            ))

        return forecasts


class WeatherAPIError(Exception):
    """Exception raised when weather API call fails."""
    pass
