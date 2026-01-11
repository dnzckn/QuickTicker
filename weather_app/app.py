"""WeatherBar - macOS Menu Bar Weather Application."""

import rumps
import threading
import logging
from typing import Optional

from .services.settings_service import SettingsService
from .services.weather_service import WeatherService, WeatherServiceError
from .ui.icons import get_icon, get_description
from .ui.menu_builder import MenuBuilder
from .models.weather_data import CompleteWeatherData
from .utils.formatters import (
    format_temp, format_wind, format_time, format_hour,
    format_pressure, format_visibility, format_uv_index,
    format_day_name
)

logger = logging.getLogger(__name__)

# Global app reference for thread updates
_app = None


class WeatherMenuBarApp(rumps.App):
    """macOS menu bar weather application."""

    def __init__(self):
        """Initialize the weather app."""
        super().__init__(
            name="WeatherBar",
            title="Loading...",
            quit_button="Quit"
        )

        global _app
        _app = self

        # Initialize services
        self.settings_service = SettingsService()
        self.weather_service = WeatherService(self.settings_service)

        # Current state
        self._weather: Optional[CompleteWeatherData] = None
        self._settings = self.settings_service.load()

        # Build static menu
        self._build_menu()

        # Set up update timer
        interval_seconds = self._settings.update_interval_minutes * 60
        self.timer = rumps.Timer(self._threaded_update, interval_seconds)
        self.timer.start()

        # Initial update
        self._threaded_update(None)

    def _build_menu(self):
        """Build the static menu structure."""
        # Location (will be updated)
        self.location_item = rumps.MenuItem("Loading location...")
        self.menu.add(self.location_item)
        self.menu.add(rumps.separator)

        # Current conditions section
        self.menu.add(rumps.MenuItem("— Current —"))
        self.condition_item = rumps.MenuItem("Loading...")
        self.menu.add(self.condition_item)
        self.feels_item = rumps.MenuItem("")
        self.menu.add(self.feels_item)
        self.humidity_item = rumps.MenuItem("")
        self.menu.add(self.humidity_item)
        self.wind_item = rumps.MenuItem("")
        self.menu.add(self.wind_item)

        self.menu.add(rumps.separator)

        # Forecast section
        self.menu.add(rumps.MenuItem("— Forecast —"))
        self.forecast_items = []
        for i in range(7):
            item = rumps.MenuItem(f"Day {i+1}")
            self.forecast_items.append(item)
            self.menu.add(item)

        self.menu.add(rumps.separator)

        # Settings submenu
        settings_menu = rumps.MenuItem("Settings")

        # Display mode
        mode_menu = rumps.MenuItem("Display Mode")
        self.essential_item = rumps.MenuItem("Essential", callback=self._set_essential)
        self.full_item = rumps.MenuItem("Full", callback=self._set_full)
        self.essential_item.state = not self._settings.is_full_mode
        self.full_item.state = self._settings.is_full_mode
        mode_menu.add(self.essential_item)
        mode_menu.add(self.full_item)
        settings_menu.add(mode_menu)

        # Temperature unit
        unit_menu = rumps.MenuItem("Temperature")
        self.fahrenheit_item = rumps.MenuItem("Fahrenheit", callback=self._set_fahrenheit)
        self.celsius_item = rumps.MenuItem("Celsius", callback=self._set_celsius)
        self.fahrenheit_item.state = self._settings.use_fahrenheit
        self.celsius_item.state = not self._settings.use_fahrenheit
        unit_menu.add(self.fahrenheit_item)
        unit_menu.add(self.celsius_item)
        settings_menu.add(unit_menu)

        # Location
        loc_menu = rumps.MenuItem("Location")
        loc_menu.add(rumps.MenuItem("Auto-detect", callback=self._auto_detect))
        loc_menu.add(rumps.MenuItem("Set Location...", callback=self._set_location))
        settings_menu.add(loc_menu)

        self.menu.add(settings_menu)

        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem("Refresh", callback=self._refresh))

        # Updated time
        self.updated_item = rumps.MenuItem("Updated: --")
        self.menu.add(self.updated_item)

    def _threaded_update(self, _):
        """Trigger weather update in background thread."""
        thread = threading.Thread(target=self._do_update, daemon=True)
        thread.start()

    def _do_update(self):
        """Fetch weather data and update UI."""
        global _app
        try:
            logger.info("Updating weather data")
            self._weather = self.weather_service.get_weather()
            self._settings = self.settings_service.load()
            self._update_display()
            logger.info("Weather update successful")
        except WeatherServiceError as e:
            logger.error(f"Weather update failed: {e}")
            if _app:
                _app.title = "⚠️ --°"
        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
            if _app:
                _app.title = "⚠️ --°"

    def _update_display(self):
        """Update all display elements."""
        global _app
        if not self._weather or not _app:
            return

        w = self._weather
        s = self._settings
        use_f = s.use_fahrenheit

        # Update title
        icon = get_icon(w.current.weather_code, w.current.is_day)
        temp = format_temp(w.current.temperature, use_f, include_unit=False)
        _app.title = f"{icon} {temp}"

        # Update location
        self.location_item.title = f"📍 {w.location_name}"

        # Update current conditions
        desc = get_description(w.current.weather_code)
        temp_full = format_temp(w.current.temperature, use_f)
        self.condition_item.title = f"{icon}  {temp_full} - {desc}"

        feels = format_temp(w.current.feels_like, use_f)
        self.feels_item.title = f"  Feels like {feels}"

        self.humidity_item.title = f"  💧 Humidity: {w.current.humidity}%"

        wind = format_wind(w.current.wind_speed, w.current.wind_direction, use_f)
        self.wind_item.title = f"  💨 Wind: {wind}"

        # Update forecast
        for i, day in enumerate(w.daily[:7]):
            if i < len(self.forecast_items):
                day_name = format_day_name(day.date)
                day_icon = get_icon(day.weather_code)
                high = format_temp(day.temp_high, use_f, include_unit=False)
                low = format_temp(day.temp_low, use_f, include_unit=False)
                self.forecast_items[i].title = f"  {day_name:8} {day_icon}  {high}/{low}"

        # Update time
        updated = w.fetched_at.strftime("%-I:%M %p")
        self.updated_item.title = f"Updated: {updated}"

    def _refresh(self, _):
        """Manual refresh."""
        self.title = "🔄 ..."
        self._threaded_update(None)

    def _set_essential(self, _):
        """Set essential display mode."""
        self.settings_service.update(display_mode="essential")
        self._settings = self.settings_service.load()
        self.essential_item.state = True
        self.full_item.state = False

    def _set_full(self, _):
        """Set full display mode."""
        self.settings_service.update(display_mode="full")
        self._settings = self.settings_service.load()
        self.essential_item.state = False
        self.full_item.state = True

    def _set_fahrenheit(self, _):
        """Set Fahrenheit units."""
        self.settings_service.update(temperature_unit="fahrenheit")
        self._settings = self.settings_service.load()
        self.fahrenheit_item.state = True
        self.celsius_item.state = False
        self._weather = None  # Force refetch
        self._threaded_update(None)

    def _set_celsius(self, _):
        """Set Celsius units."""
        self.settings_service.update(temperature_unit="celsius")
        self._settings = self.settings_service.load()
        self.fahrenheit_item.state = False
        self.celsius_item.state = True
        self._weather = None  # Force refetch
        self._threaded_update(None)

    def _auto_detect(self, _):
        """Auto-detect location."""
        self.title = "🔍 ..."

        def do_detect():
            try:
                self.weather_service.auto_detect_location()
                self._threaded_update(None)
            except Exception as e:
                logger.error(f"Auto-detect failed: {e}")

        thread = threading.Thread(target=do_detect, daemon=True)
        thread.start()

    def _set_location(self, _):
        """Set location manually."""
        window = rumps.Window(
            message="Enter city name:",
            title="Set Location",
            default_text="",
            ok="Search",
            cancel="Cancel",
            dimensions=(300, 24)
        )
        response = window.run()

        if not response.clicked or not response.text.strip():
            return

        query = response.text.strip()
        locations = self.weather_service.search_locations(query)

        if not locations:
            rumps.alert("No Results", f"No locations found for '{query}'")
            return

        if len(locations) == 1:
            selected = locations[0]
        else:
            msg = "Select a location:\n\n"
            for i, loc in enumerate(locations, 1):
                msg += f"{i}. {loc.display_name}\n"

            select_window = rumps.Window(
                message=msg,
                title="Select",
                default_text="1",
                ok="OK",
                cancel="Cancel"
            )
            resp = select_window.run()

            if not resp.clicked:
                return

            try:
                idx = int(resp.text.strip()) - 1
                if 0 <= idx < len(locations):
                    selected = locations[idx]
                else:
                    return
            except ValueError:
                return

        self.weather_service.set_location(selected)
        self._threaded_update(None)


def run():
    """Run the weather app."""
    app = WeatherMenuBarApp()
    app.run()
