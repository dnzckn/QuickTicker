#!/bin/bash
# WeatherBar - macOS Menu Bar Weather App
# Kill any existing instance
killall -9 Python 2>/dev/null || true

# Run the new weather app
/Users/deniz/anaconda3/envs/ds310/bin/python3 /Users/deniz/Documents/GitHub/QuickTicker/weather_app/main.py
