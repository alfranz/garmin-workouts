import logging
import garth
from typing import Optional, Dict, Any
import os
from garminworkouts.models.workout import Workout

logger = logging.getLogger(__name__)


class GarminException(Exception):
    """Base exception for all exceptions."""

    msg: str


class GarminClient:
    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        if not username and os.getenv("GARMIN_USERNAME") is None:
            raise GarminException("Username is required")
        if not password and os.getenv("GARMIN_PASSWORD") is None:
            raise GarminException("Password is required")

        self.username = os.getenv("GARMIN_USERNAME") if username is None else "username"
        self.password = os.getenv("GARMIN_PASSWORD") if password is None else "password"
        self.garth = garth.Client(domain="garmin.com")

        self.garmin_connect_user_settings_url = (
            "/userprofile-service/userprofile/user-settings"
        )
        self.garmin_workouts = "/workout-service"
        self.garmin_connect_hrv_url = "/hrv-service/hrv"

        self.prompt_mfa = None

    def connectapi(self, path, **kwargs):
        return self.garth.connectapi(path, **kwargs)

    def login(self):
        """Log in using Garth."""

        self.garth.login(self.username, self.password)
        self.display_name = self.garth.profile["displayName"]
        self.full_name = self.garth.profile["fullName"]

        settings = self.garth.connectapi(self.garmin_connect_user_settings_url)
        self.unit_system = settings["userData"]["measurementSystem"]

        return True

    def get_workouts(self, batch_size: int = 100):
        """Return workouts from start till end."""

        url = f"{self.garmin_workouts}/workouts"

        response_jsons = []
        start_index = 0
        end = start_index + batch_size
        logger.debug(f"Requesting workouts from {start_index}-{end}")
        params = {"start": 0, "limit": batch_size}
        response = self.connectapi(url, params=params)
        response_jsons.extend(response)
        return response_jsons

    def get_workout_by_id(self, workout_id: str):
        """Return workout by id."""

        url = f"{self.garmin_workouts}/workout/{workout_id}"
        return self.connectapi(url)

    def get_hrv_data(self, date: str) -> Dict[str, Any]:
        """Return Heart Rate Variability (hrv) data for current user."""

        url = f"{self.garmin_connect_hrv_url}/{date}"
        logger.debug("Requesting Heart Rate Variability (hrv) data")

        return self.connectapi(url)

    def save_workout(self, workout: Workout):
        url = f"{self.garmin_workouts}/workouts"
        payload = workout.create_workout()
        return self.garth.post("connectapi", url, json=payload)

    def update_workout(self, workout_id: str, workout: Workout):
        url = f"{self.garmin_workouts}/workouts/{workout_id}"

        payload = workout.create_workout()
        return self.garth.post("connectapi", url, json=payload)

    def delete_workout(self, workout_id: str):
        url = f"{self.garmin_workouts}/workouts/{workout_id}"
        return self.garth.request(
            "DELETE",
            "connectapi",
            url,
            api=True,
        )

    def schedule_workout(self, workout_id: str, date: str):
        url = f"{self.garmin_workouts}/schedule/{workout_id}"
        payload = {"date": date}
        return self.garth.post("connectapi", url, json=payload)
