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
        adjusted_pace = self.minutes_per_km
        return max(adjusted_pace, 0)

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
