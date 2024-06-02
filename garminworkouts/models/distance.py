from dataclasses import dataclass, field
import re


@dataclass
class Distance:
    distance_str: str
    distance_meters: float = field(init=False)

    def __post_init__(self):
        self.distance_meters = self._parse_distance(self.distance_str)

    def _parse_distance(self, distance_str: str) -> float:
        match = re.match(
            r"(\d*\.?\d+)\s*(m|meters?|kms?|kilometers?)", distance_str, re.IGNORECASE
        )
        if not match:
            raise ValueError(f"Invalid distance format: '{distance_str}'")

        value = float(match.group(1))
        unit = match.group(2).lower()

        if unit in ["km", "kms", "kilometer", "kilometers"]:
            return value * 1000
        elif unit in ["m", "meter", "meters"]:
            return value
        else:
            raise ValueError(f"Unknown unit in distance: '{unit}'")
