class Pace:
    def __init__(self, pace_str):
        # Expecting pace_str in the format "min:sec/km" (e.g., "5:00")
        self.pace_str = pace_str
        self.minutes_per_km = self._parse_time(pace_str)

    def _parse_time(self, time_str):
        # Convert "min:sec" string to float representing minutes
        if time_str.startswith("-"):
            negative = True
            time_str = time_str[1:]
        else:
            negative = False

        minutes, seconds = map(int, time_str.split(":"))
        total_minutes = minutes + seconds / 60.0
        return -total_minutes if negative else total_minutes

    def to_min_per_km(self, diff_str=None):
        # Return the pace as min/km with optional difference applied
        if diff_str:
            diff_minutes = self._parse_time(diff_str)
            adjusted_pace = self.minutes_per_km + diff_minutes
        else:
            adjusted_pace = self.minutes_per_km
        return max(adjusted_pace, 0)  # Ensure pace is not negative

    def __eq__(self, other):
        if not isinstance(other, Pace):
            return False
        return self.minutes_per_km == other.minutes_per_km

    def __str__(self):
        # Convert minutes per km back to "min:sec/km" format
        total_seconds = int(self.minutes_per_km * 60)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:02d}"
