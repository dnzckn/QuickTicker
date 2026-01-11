#!/usr/bin/env python3
"""WeatherBar - macOS Menu Bar Weather Application.

Entry point for the application.
"""

import sys
import os

# Add parent directory to path for imports when running directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from weather_app.utils.logger import setup_logging, get_logger
from weather_app.app import run


def main():
    """Main entry point."""
    # Set up logging
    setup_logging(debug=False)
    logger = get_logger(__name__)

    logger.info("Starting WeatherBar application")

    try:
        run()
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
