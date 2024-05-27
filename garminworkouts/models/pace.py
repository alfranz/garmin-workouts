class Pace:
    def __init__(self, pace_str: str):
        # Expecting pace_str in the format "min:sec/km" (e.g., "5:00")
        self.pace_str = pace_str
        self.minutes_per_km = self._parse_time(pace_str)

    def _parse_time(self, time_str: str) -> float:
        # Convert "min:sec" string to float representing minutes
        if time_str.startswith("-"):
            raise ValueError("Negative paces are not supported")
        if time_str.count(":") != 1:
            raise ValueError(f"Invalid time format: {time_str} - Should be 'min:sec'")

        minutes, seconds = map(int, time_str.split(":"))
        total_minutes = minutes + seconds / 60.0
        return total_minutes

    def to_min_per_km(self) -> float:
        return self.minutes_per_km

    def to_m_per_s(self) -> float:
        sec_per_km = self.minutes_per_km * 60
        # sec/km to m/s
        return 1000 / sec_per_km

    def to_garmin(self) -> float:
        # alias for to_m_per_s
        return self.to_m_per_s()

    def __eq__(self, other):
        if not isinstance(other, Pace):
            return False
        return self.minutes_per_km == other.minutes_per_km

    def __ge__(self, other):
        # Note: GE refers to more minutes per km NOT faster pace
        return self.minutes_per_km >= other.minutes_per_km

    def __ne__(self, other):
        return not self.__eq__(other)

    def __le__(self, other):
        return self.minutes_per_km <= other.minutes_per_km

    def __gt__(self, other):
        return self.minutes_per_km > other.minutes_per_km

    def __lt__(self, other):
        return self.minutes_per_km < other.minutes_per_km

    def __str__(self):
        # Convert minutes per km back to "min:sec/km" format
        total_seconds = int(self.minutes_per_km * 60)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:02d}"


class PaceRange:
    def __init__(self, name: str, lower: str, upper: str):
        self.name = name
        if not (lower <= upper):
            raise ValueError("Lower pace must be less or equal to upper pace")
        self.lower = Pace(lower)
        self.upper = Pace(upper)

    @property
    def bounds(self) -> tuple[Pace, Pace]:
        return (self.lower, self.upper)

    def __str__(self) -> str:
        return f"{self.name}: {str(self.lower)} - {str(self.upper)}"

    def contains(self, pace: Pace) -> bool:
        return (
            self.lower.to_min_per_km()
            <= pace.to_min_per_km()
            <= self.upper.to_min_per_km()
        )