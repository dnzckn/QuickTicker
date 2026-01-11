from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Location:
    """Represents a geographic location."""
    name: str
    latitude: float
    longitude: float
    country: str
    timezone: str
    country_code: Optional[str] = None
    admin1: Optional[str] = None  # State/Province

    @property
    def display_name(self) -> str:
        """Format location for display (e.g., 'San Diego, CA')."""
        if self.admin1 and self.country_code == "US":
            # US states: use state abbreviation
            return f"{self.name}, {self.admin1}"
        elif self.admin1:
            return f"{self.name}, {self.admin1}, {self.country}"
        else:
            return f"{self.name}, {self.country}"

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Location':
        """Create Location from dictionary."""
        return cls(
            name=data.get('name', ''),
            latitude=data.get('latitude', 0.0),
            longitude=data.get('longitude', 0.0),
            country=data.get('country', ''),
            timezone=data.get('timezone', 'UTC'),
            country_code=data.get('country_code'),
            admin1=data.get('admin1')
        )

    @classmethod
    def default(cls) -> 'Location':
        """Default location: San Diego, CA."""
        return cls(
            name="San Diego",
            latitude=32.7157,
            longitude=-117.1611,
            country="United States",
            timezone="America/Los_Angeles",
            country_code="US",
            admin1="California"
        )
