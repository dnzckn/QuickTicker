"""Build rumps menu structure from weather data."""

import rumps
from datetime import datetime
from typing import List, Callable, Optional

from ..models.weather_data import CompleteWeatherData, DailyForecast, HourlyForecast
from ..models.settings import Settings
from .icons import get_icon, get_description
from ..utils.formatters import (
    format_temp, format_wind, format_time, format_hour,
    format_pressure, format_visibility, format_uv_index,
    format_day_name, format_percent
)


class MenuBuilder:
    """Builds rumps menu structure from weather data."""

    def __init__(self, callbacks: dict):
        """
        Initialize MenuBuilder with callback functions.

        Args:
            callbacks: Dictionary mapping callback names to functions
                - 'toggle_mode': Toggle between full/essential mode
                - 'set_unit_fahrenheit': Set temperature to Fahrenheit
                - 'set_unit_celsius': Set temperature to Celsius
                - 'set_interval': Set update interval (receives minutes)
                - 'auto_detect': Auto-detect location
                - 'set_location': Open location dialog
                - 'refresh': Refresh weather data
        """
        self.callbacks = callbacks

    def build_menu_title(self, weather: CompleteWeatherData, settings: Settings) -> str:
        """
        Build menu bar title string.

        Args:
            weather: Current weather data
            settings: Current settings

        Returns:
            Menu bar title (e.g., "sun.max.fill 72")
        """
        icon = get_icon(weather.current.weather_code, weather.current.is_day)
        temp = format_temp(weather.current.temperature, settings.use_fahrenheit, include_unit=False)
        return f"{icon} {temp}"

    def build_menu(self, weather: Optional[CompleteWeatherData], settings: Settings) -> List[rumps.MenuItem]:
        """
        Build complete menu based on current mode.

        Args:
            weather: Current weather data (or None if not available)
            settings: Current settings

        Returns:
            List of menu items
        """
        items = []

        if weather is None:
            items.append(rumps.MenuItem("Loading weather data..."))
            items.append(rumps.separator)
        elif settings.is_full_mode:
            items.extend(self._build_full_menu(weather, settings))
        else:
            items.extend(self._build_essential_menu(weather, settings))

        # Settings submenu
        items.append(rumps.separator)
        items.append(self._build_settings_menu(settings))

        # Refresh and status
        items.append(rumps.separator)
        refresh_item = rumps.MenuItem("Refresh Now", callback=self.callbacks.get('refresh'))
        items.append(refresh_item)

        if weather:
            updated = weather.fetched_at.strftime("%-I:%M %p")
            items.append(rumps.MenuItem(f"Updated: {updated}"))

        return items

    def _build_essential_menu(self, weather: CompleteWeatherData, settings: Settings) -> List[rumps.MenuItem]:
        """Build essential mode menu items."""
        items = []

        # Location header
        items.append(rumps.MenuItem(f"\U0001F4CD {weather.location_name}"))
        items.append(rumps.separator)

        # Current conditions
        icon = get_icon(weather.current.weather_code, weather.current.is_day)
        desc = get_description(weather.current.weather_code)
        temp = format_temp(weather.current.temperature, settings.use_fahrenheit)
        items.append(rumps.MenuItem(f"{icon}  {temp} - {desc}"))

        # Humidity and High/Low
        today = weather.today
        if today:
            high = format_temp(today.temp_high, settings.use_fahrenheit, include_unit=False)
            low = format_temp(today.temp_low, settings.use_fahrenheit, include_unit=False)
            items.append(rumps.MenuItem(f"\U0001F4A7 {weather.current.humidity}%  |  High: {high}  |  Low: {low}"))

        # 3-day forecast
        items.append(rumps.separator)
        items.append(rumps.MenuItem("\u2014 3-Day Forecast \u2014"))

        for day in weather.daily[:3]:
            day_str = format_day_name(day.date)
            icon = get_icon(day.weather_code)
            high = format_temp(day.temp_high, settings.use_fahrenheit, include_unit=False)
            low = format_temp(day.temp_low, settings.use_fahrenheit, include_unit=False)
            items.append(rumps.MenuItem(f"  {day_str:8} {icon}  {high}/{low}"))

        return items

    def _build_full_menu(self, weather: CompleteWeatherData, settings: Settings) -> List[rumps.MenuItem]:
        """Build full mode menu items."""
        items = []
        use_f = settings.use_fahrenheit

        # Location header
        items.append(rumps.MenuItem(f"\U0001F4CD {weather.location_name}"))
        items.append(rumps.separator)

        # Current Conditions section
        items.append(rumps.MenuItem("\u2014 Current Conditions \u2014"))

        icon = get_icon(weather.current.weather_code, weather.current.is_day)
        desc = get_description(weather.current.weather_code)
        temp = format_temp(weather.current.temperature, use_f)
        feels = format_temp(weather.current.feels_like, use_f)
        items.append(rumps.MenuItem(f"  {icon}  {temp} ({desc})"))
        items.append(rumps.MenuItem(f"  Feels like {feels}"))
        items.append(rumps.MenuItem(f"  \U0001F4A7 Humidity: {weather.current.humidity}%"))
        items.append(rumps.MenuItem(f"  \U0001F4A8 Wind: {format_wind(weather.current.wind_speed, weather.current.wind_direction, use_f)}"))
        items.append(rumps.MenuItem(f"  \U0001F4CA Pressure: {format_pressure(weather.current.pressure)}"))
        items.append(rumps.MenuItem(f"  \U0001F441 Visibility: {format_visibility(weather.current.visibility, use_f)}"))
        items.append(rumps.MenuItem(f"  \u2600\ufe0f UV Index: {format_uv_index(weather.current.uv_index)}"))

        # Sun section
        today = weather.today
        if today:
            items.append(rumps.separator)
            items.append(rumps.MenuItem("\u2014 Sun \u2014"))
            items.append(rumps.MenuItem(f"  \U0001F305 Sunrise: {format_time(today.sunrise)}"))
            items.append(rumps.MenuItem(f"  \U0001F307 Sunset: {format_time(today.sunset)}"))

        # Hourly forecast section (next 6 hours)
        items.append(rumps.separator)
        items.append(rumps.MenuItem("\u2014 Hourly Forecast \u2014"))
        for hour in weather.hourly[:6]:
            hour_str = format_hour(hour.time)
            icon = get_icon(hour.weather_code)
            temp = format_temp(hour.temperature, use_f, include_unit=False)
            precip = f" {format_percent(hour.precipitation_probability)}" if hour.precipitation_probability > 0 else ""
            items.append(rumps.MenuItem(f"  {hour_str:8} {icon}  {temp}{precip}"))

        # Daily forecast section
        items.append(rumps.separator)
        items.append(rumps.MenuItem("\u2014 7-Day Forecast \u2014"))
        for day in weather.daily:
            day_str = format_day_name(day.date)
            icon = get_icon(day.weather_code)
            high = format_temp(day.temp_high, use_f, include_unit=False)
            low = format_temp(day.temp_low, use_f, include_unit=False)
            precip = f" \U0001F4A7{day.precipitation_probability}%" if day.precipitation_probability > 10 else ""
            items.append(rumps.MenuItem(f"  {day_str:8} {icon}  {high}/{low}{precip}"))

        return items

    def _build_settings_menu(self, settings: Settings) -> rumps.MenuItem:
        """Build settings submenu."""
        settings_menu = rumps.MenuItem("\u2699\ufe0f Settings")

        # Display Mode submenu
        mode_menu = rumps.MenuItem("Display Mode")
        essential_item = rumps.MenuItem(
            "Essential",
            callback=lambda _: self.callbacks.get('set_mode', lambda x: None)('essential')
        )
        essential_item.state = not settings.is_full_mode
        mode_menu.add(essential_item)

        full_item = rumps.MenuItem(
            "Full",
            callback=lambda _: self.callbacks.get('set_mode', lambda x: None)('full')
        )
        full_item.state = settings.is_full_mode
        mode_menu.add(full_item)
        settings_menu.add(mode_menu)

        # Temperature Unit submenu
        unit_menu = rumps.MenuItem("Temperature")
        f_item = rumps.MenuItem(
            "Fahrenheit (\u00b0F)",
            callback=lambda _: self.callbacks.get('set_unit', lambda x: None)('fahrenheit')
        )
        f_item.state = settings.use_fahrenheit
        unit_menu.add(f_item)

        c_item = rumps.MenuItem(
            "Celsius (\u00b0C)",
            callback=lambda _: self.callbacks.get('set_unit', lambda x: None)('celsius')
        )
        c_item.state = not settings.use_fahrenheit
        unit_menu.add(c_item)
        settings_menu.add(unit_menu)

        # Update Interval submenu
        interval_menu = rumps.MenuItem("Update Interval")
        for minutes in [5, 10, 15, 30]:
            interval_item = rumps.MenuItem(
                f"{minutes} minutes",
                callback=lambda _, m=minutes: self.callbacks.get('set_interval', lambda x: None)(m)
            )
            interval_item.state = settings.update_interval_minutes == minutes
            interval_menu.add(interval_item)
        settings_menu.add(interval_menu)

        # Location submenu
        location_menu = rumps.MenuItem("Location")
        auto_item = rumps.MenuItem(
            "\U0001F50D Auto-detect",
            callback=self.callbacks.get('auto_detect')
        )
        location_menu.add(auto_item)

        set_item = rumps.MenuItem(
            "\U0001F4DD Set Location...",
            callback=self.callbacks.get('set_location')
        )
        location_menu.add(set_item)

        if settings.location:
            location_menu.add(rumps.separator)
            current_item = rumps.MenuItem(f"\u2713 {settings.location.display_name}")
            location_menu.add(current_item)

        settings_menu.add(location_menu)

        return settings_menu

    def build_error_menu(self, error_message: str, settings: Settings) -> List[rumps.MenuItem]:
        """Build menu when weather data is unavailable."""
        items = []
        items.append(rumps.MenuItem("\u26a0\ufe0f Weather Unavailable"))
        items.append(rumps.MenuItem(f"  {error_message}"))
        items.append(rumps.separator)
        items.append(self._build_settings_menu(settings))
        items.append(rumps.separator)
        items.append(rumps.MenuItem("Refresh Now", callback=self.callbacks.get('refresh')))
        return items
