from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class CurrentWeather:
    """Current weather conditions."""
    temperature: float
    feels_like: float
    humidity: int
    wind_speed: float
    wind_direction: int
    pressure: float
    visibility: float
    uv_index: float
    weather_code: int
    is_day: bool
    timestamp: datetime

    @classmethod
    def from_api_response(cls, data: dict, current_data: dict) -> 'CurrentWeather':
        """Create from Open-Meteo API response."""
        return cls(
            temperature=current_data.get('temperature_2m', 0),
            feels_like=current_data.get('apparent_temperature', 0),
            humidity=int(current_data.get('relative_humidity_2m', 0)),
            wind_speed=current_data.get('wind_speed_10m', 0),
            wind_direction=int(current_data.get('wind_direction_10m', 0)),
            pressure=current_data.get('pressure_msl', 0),
            visibility=current_data.get('visibility', 0),
            uv_index=current_data.get('uv_index', 0),
            weather_code=int(current_data.get('weather_code', 0)),
            is_day=bool(current_data.get('is_day', 1)),
            timestamp=datetime.fromisoformat(current_data.get('time', datetime.now().isoformat()))
        )


@dataclass
class HourlyForecast:
    """Hourly weather forecast."""
    time: datetime
    temperature: float
    weather_code: int
    precipitation_probability: int

    @classmethod
    def from_api_data(cls, time_str: str, temp: float, code: int, precip: int) -> 'HourlyForecast':
        """Create from individual API data points."""
        return cls(
            time=datetime.fromisoformat(time_str),
            temperature=temp,
            weather_code=int(code),
            precipitation_probability=int(precip) if precip is not None else 0
        )


@dataclass
class DailyForecast:
    """Daily weather forecast."""
    date: datetime
    temp_high: float
    temp_low: float
    weather_code: int
    precipitation_probability: int
    uv_index_max: float
    sunrise: datetime
    sunset: datetime

    @classmethod
    def from_api_data(cls, date_str: str, temp_max: float, temp_min: float,
                      code: int, precip: int, uv: float,
                      sunrise_str: str, sunset_str: str) -> 'DailyForecast':
        """Create from individual API data points."""
        return cls(
            date=datetime.fromisoformat(date_str),
            temp_high=temp_max,
            temp_low=temp_min,
            weather_code=int(code),
            precipitation_probability=int(precip) if precip is not None else 0,
            uv_index_max=uv if uv is not None else 0,
            sunrise=datetime.fromisoformat(sunrise_str),
            sunset=datetime.fromisoformat(sunset_str)
        )


@dataclass
class CompleteWeatherData:
    """Complete weather data including current, hourly, and daily forecasts."""
    current: CurrentWeather
    hourly: List[HourlyForecast]
    daily: List[DailyForecast]
    location_name: str
    fetched_at: datetime = None

    def __post_init__(self):
        if self.fetched_at is None:
            self.fetched_at = datetime.now()

    @property
    def today(self) -> Optional[DailyForecast]:
        """Get today's forecast."""
        if self.daily:
            return self.daily[0]
        return None
