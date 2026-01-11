"""Formatting utilities for weather data display."""

from datetime import datetime


def format_temp(temp: float, use_fahrenheit: bool = True, include_unit: bool = True) -> str:
    """
    Format temperature for display.

    Args:
        temp: Temperature value
        use_fahrenheit: If True, display as Fahrenheit; otherwise Celsius
        include_unit: If True, include degree symbol and unit

    Returns:
        Formatted temperature string
    """
    temp_rounded = round(temp)
    if include_unit:
        unit = "F" if use_fahrenheit else "C"
        return f"{temp_rounded}\u00b0{unit}"
    return f"{temp_rounded}\u00b0"


def format_wind(speed: float, direction: int, use_mph: bool = True) -> str:
    """
    Format wind speed and direction for display.

    Args:
        speed: Wind speed
        direction: Wind direction in degrees (0-360)
        use_mph: If True, use mph; otherwise km/h

    Returns:
        Formatted wind string (e.g., "8 mph NW")
    """
    # Convert degrees to compass direction
    compass = get_compass_direction(direction)
    unit = "mph" if use_mph else "km/h"
    return f"{round(speed)} {unit} {compass}"


def get_compass_direction(degrees: int) -> str:
    """
    Convert degrees to compass direction.

    Args:
        degrees: Wind direction in degrees (0-360)

    Returns:
        Compass direction (N, NE, E, etc.)
    """
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                  "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = round(degrees / 22.5) % 16
    return directions[index]


def format_time(dt: datetime, use_12h: bool = True) -> str:
    """
    Format time for display.

    Args:
        dt: Datetime object
        use_12h: If True, use 12-hour format; otherwise 24-hour

    Returns:
        Formatted time string
    """
    if use_12h:
        return dt.strftime("%-I:%M %p")
    return dt.strftime("%H:%M")


def format_hour(dt: datetime, use_12h: bool = True) -> str:
    """
    Format hour only for display.

    Args:
        dt: Datetime object
        use_12h: If True, use 12-hour format

    Returns:
        Formatted hour string (e.g., "3 PM" or "15")
    """
    if use_12h:
        return dt.strftime("%-I %p")
    return dt.strftime("%H")


def format_pressure(pressure: float) -> str:
    """
    Format pressure for display.

    Args:
        pressure: Pressure in hPa (millibars)

    Returns:
        Formatted pressure string
    """
    return f"{round(pressure)} hPa"


def format_visibility(visibility: float, use_miles: bool = True) -> str:
    """
    Format visibility for display.

    Args:
        visibility: Visibility in meters
        use_miles: If True, convert to miles; otherwise km

    Returns:
        Formatted visibility string
    """
    if use_miles:
        # Convert meters to miles
        miles = visibility / 1609.34
        if miles >= 10:
            return f"{round(miles)} mi"
        return f"{miles:.1f} mi"
    else:
        # Convert to km
        km = visibility / 1000
        if km >= 10:
            return f"{round(km)} km"
        return f"{km:.1f} km"


def format_uv_index(uv: float) -> str:
    """
    Format UV index with risk level.

    Args:
        uv: UV index value

    Returns:
        Formatted UV string with risk level
    """
    uv_rounded = round(uv, 1)
    if uv < 3:
        level = "Low"
    elif uv < 6:
        level = "Moderate"
    elif uv < 8:
        level = "High"
    elif uv < 11:
        level = "Very High"
    else:
        level = "Extreme"

    return f"{uv_rounded} ({level})"


def format_day_name(dt: datetime, include_today: bool = True) -> str:
    """
    Format date as day name.

    Args:
        dt: Datetime object
        include_today: If True, return "Today" for current date

    Returns:
        Day name (e.g., "Today", "Mon", "Tue")
    """
    today = datetime.now().date()
    if include_today and dt.date() == today:
        return "Today"
    return dt.strftime("%a")


def format_percent(value: int) -> str:
    """
    Format percentage value.

    Args:
        value: Percentage value (0-100)

    Returns:
        Formatted percentage string
    """
    return f"{value}%"
