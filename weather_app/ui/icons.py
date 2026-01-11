"""Weather condition icons and descriptions based on WMO weather codes."""

# WMO Weather Code to Emoji Mapping
# https://open-meteo.com/en/docs (see weather_code in API docs)
WEATHER_ICONS_DAY = {
    0: "sun",       # Clear sky
    1: "sun.max",   # Mainly clear
    2: "cloud.sun", # Partly cloudy
    3: "cloud",     # Overcast
    45: "cloud.fog",    # Fog
    48: "cloud.fog",    # Depositing rime fog
    51: "cloud.drizzle", # Light drizzle
    53: "cloud.drizzle", # Moderate drizzle
    55: "cloud.drizzle", # Dense drizzle
    56: "cloud.sleet",   # Light freezing drizzle
    57: "cloud.sleet",   # Dense freezing drizzle
    61: "cloud.rain",    # Slight rain
    63: "cloud.rain",    # Moderate rain
    65: "cloud.heavyrain", # Heavy rain
    66: "cloud.sleet",   # Light freezing rain
    67: "cloud.sleet",   # Heavy freezing rain
    71: "cloud.snow",    # Slight snow
    73: "cloud.snow",    # Moderate snow
    75: "snow",          # Heavy snow
    77: "cloud.snow",    # Snow grains
    80: "cloud.sun.rain", # Slight rain showers
    81: "cloud.rain",    # Moderate rain showers
    82: "cloud.heavyrain", # Violent rain showers
    85: "cloud.snow",    # Slight snow showers
    86: "cloud.snow",    # Heavy snow showers
    95: "cloud.bolt",    # Thunderstorm
    96: "cloud.bolt.rain", # Thunderstorm with slight hail
    99: "cloud.bolt.rain", # Thunderstorm with heavy hail
}

# Emoji alternatives (for menu bar display)
WEATHER_EMOJIS = {
    0: "sun.max.fill",      # Clear sky
    1: "sun.max",   # Mainly clear
    2: "cloud.sun.fill", # Partly cloudy
    3: "cloud.fill",     # Overcast
    45: "cloud.fog.fill",    # Fog
    48: "cloud.fog.fill",    # Depositing rime fog
    51: "cloud.drizzle.fill", # Light drizzle
    53: "cloud.drizzle.fill", # Moderate drizzle
    55: "cloud.drizzle.fill", # Dense drizzle
    56: "cloud.sleet.fill",   # Light freezing drizzle
    57: "cloud.sleet.fill",   # Dense freezing drizzle
    61: "cloud.rain.fill",    # Slight rain
    63: "cloud.rain.fill",    # Moderate rain
    65: "cloud.heavyrain.fill", # Heavy rain
    66: "cloud.sleet.fill",   # Light freezing rain
    67: "cloud.sleet.fill",   # Heavy freezing rain
    71: "cloud.snow.fill",    # Slight snow
    73: "cloud.snow.fill",    # Moderate snow
    75: "snowflake",          # Heavy snow
    77: "cloud.snow.fill",    # Snow grains
    80: "cloud.sun.rain.fill", # Slight rain showers
    81: "cloud.rain.fill",    # Moderate rain showers
    82: "cloud.heavyrain.fill", # Violent rain showers
    85: "cloud.snow.fill",    # Slight snow showers
    86: "cloud.snow.fill",    # Heavy snow showers
    95: "cloud.bolt.fill",    # Thunderstorm
    96: "cloud.bolt.rain.fill", # Thunderstorm with slight hail
    99: "cloud.bolt.rain.fill", # Thunderstorm with heavy hail
}

# Text emojis for menu display
TEXT_EMOJIS = {
    0: "\u2600\ufe0f",      # Clear sky - sun
    1: "\U0001F324\ufe0f",  # Mainly clear - sun behind small cloud
    2: "\u26c5",            # Partly cloudy
    3: "\u2601\ufe0f",      # Overcast - cloud
    45: "\U0001F32B\ufe0f", # Fog
    48: "\U0001F32B\ufe0f", # Depositing rime fog
    51: "\U0001F326\ufe0f", # Light drizzle
    53: "\U0001F326\ufe0f", # Moderate drizzle
    55: "\U0001F327\ufe0f", # Dense drizzle
    56: "\U0001F327\ufe0f", # Light freezing drizzle
    57: "\U0001F327\ufe0f", # Dense freezing drizzle
    61: "\U0001F327\ufe0f", # Slight rain
    63: "\U0001F327\ufe0f", # Moderate rain
    65: "\U0001F327\ufe0f", # Heavy rain
    66: "\U0001F327\ufe0f", # Light freezing rain
    67: "\U0001F327\ufe0f", # Heavy freezing rain
    71: "\U0001F328\ufe0f", # Slight snow
    73: "\U0001F328\ufe0f", # Moderate snow
    75: "\u2744\ufe0f",     # Heavy snow - snowflake
    77: "\U0001F328\ufe0f", # Snow grains
    80: "\U0001F326\ufe0f", # Slight rain showers
    81: "\U0001F326\ufe0f", # Moderate rain showers
    82: "\u26c8\ufe0f",     # Violent rain showers - thunder cloud
    85: "\U0001F328\ufe0f", # Slight snow showers
    86: "\U0001F328\ufe0f", # Heavy snow showers
    95: "\u26c8\ufe0f",     # Thunderstorm
    96: "\u26c8\ufe0f",     # Thunderstorm with slight hail
    99: "\u26c8\ufe0f",     # Thunderstorm with heavy hail
}

# Night variants (replace sun with moon)
NIGHT_EMOJIS = {
    0: "\U0001F319",        # Clear night - crescent moon
    1: "\U0001F319",        # Mainly clear night
    2: "\u2601\ufe0f",      # Partly cloudy night (cloud)
}

# Weather descriptions
WEATHER_DESCRIPTIONS = {
    0: "Clear",
    1: "Mostly Clear",
    2: "Partly Cloudy",
    3: "Cloudy",
    45: "Foggy",
    48: "Foggy",
    51: "Light Drizzle",
    53: "Drizzle",
    55: "Heavy Drizzle",
    56: "Freezing Drizzle",
    57: "Freezing Drizzle",
    61: "Light Rain",
    63: "Rain",
    65: "Heavy Rain",
    66: "Freezing Rain",
    67: "Freezing Rain",
    71: "Light Snow",
    73: "Snow",
    75: "Heavy Snow",
    77: "Snow Grains",
    80: "Light Showers",
    81: "Showers",
    82: "Heavy Showers",
    85: "Snow Showers",
    86: "Heavy Snow Showers",
    95: "Thunderstorm",
    96: "Thunderstorm",
    99: "Severe Thunderstorm",
}


def get_icon(weather_code: int, is_day: bool = True) -> str:
    """
    Get emoji icon for weather code.

    Args:
        weather_code: WMO weather code
        is_day: Whether it's daytime (affects clear sky icons)

    Returns:
        Emoji string for the weather condition
    """
    if not is_day and weather_code in NIGHT_EMOJIS:
        return NIGHT_EMOJIS[weather_code]
    return TEXT_EMOJIS.get(weather_code, "\u2753")  # Default: question mark


def get_sf_symbol(weather_code: int, is_day: bool = True) -> str:
    """
    Get SF Symbol name for weather code.

    Args:
        weather_code: WMO weather code
        is_day: Whether it's daytime

    Returns:
        SF Symbol name string
    """
    if not is_day:
        # Return night variants for clear conditions
        if weather_code == 0:
            return "moon.stars.fill"
        elif weather_code == 1:
            return "moon.fill"
        elif weather_code == 2:
            return "cloud.moon.fill"

    return WEATHER_EMOJIS.get(weather_code, "questionmark.circle")


def get_description(weather_code: int) -> str:
    """
    Get text description for weather code.

    Args:
        weather_code: WMO weather code

    Returns:
        Human-readable weather description
    """
    return WEATHER_DESCRIPTIONS.get(weather_code, "Unknown")
