from dataclasses import dataclass, asdict, field
from typing import Optional
from .location import Location


@dataclass
class Settings:
    """Application settings."""
    display_mode: str = "essential"  # "essential" or "full"
    temperature_unit: str = "fahrenheit"  # "fahrenheit" or "celsius"
    update_interval_minutes: int = 15
    location_mode: str = "auto"  # "auto" or "manual"
    location: Optional[Location] = None
    version: int = 1

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        data = {
            'version': self.version,
            'display_mode': self.display_mode,
            'temperature_unit': self.temperature_unit,
            'update_interval_minutes': self.update_interval_minutes,
            'location_mode': self.location_mode,
            'location': self.location.to_dict() if self.location else None
        }
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'Settings':
        """Create Settings from dictionary."""
        location_data = data.get('location')
        location = Location.from_dict(location_data) if location_data else None

        return cls(
            version=data.get('version', 1),
            display_mode=data.get('display_mode', 'essential'),
            temperature_unit=data.get('temperature_unit', 'fahrenheit'),
            update_interval_minutes=data.get('update_interval_minutes', 15),
            location_mode=data.get('location_mode', 'auto'),
            location=location
        )

    @classmethod
    def default(cls) -> 'Settings':
        """Create default settings."""
        return cls()

    @property
    def use_fahrenheit(self) -> bool:
        return self.temperature_unit == "fahrenheit"

    @property
    def is_full_mode(self) -> bool:
        return self.display_mode == "full"
