import glob
import logging
import typer
from typing import Optional
from typing_extensions import Annotated

from garminworkouts.config.configreader import read_workout
from garminworkouts.garmin.garminclient import GarminClient

from garminworkouts.models.workout import Workout
from garminworkouts.models.running_workout import RunningWorkout

app = typer.Typer(no_args_is_help=True)


def _garmin_client(
    username: Optional[str],
    password: Optional[str],
) -> GarminClient:
    client = GarminClient(
        username=username,
        password=password,
    )
    client.login()
    return client


@app.command(no_args_is_help=True)
def sync(
    workouts_path: Annotated[
        str,
        typer.Argument(
            help="File(s) with workout(s) to import, wildcards are supported e.g: sample_workouts/*.yaml"
        ),
    ],
    username: Annotated[
        Optional[str],
        typer.Argument(
            envvar="GARMIN_USERNAME", help="Garmin Connect account username"
        ),
    ],
    password: Annotated[
        Optional[str],
        typer.Argument(
            envvar="GARMIN_PASSWORD",
            help="Garmin Connect account password",
        ),
    ],
):
    """
    Sync your local workouts with Garmin Connect.
    """
    workout_files = glob.glob(workouts_path)
    workouts = [read_workout(workout_file) for workout_file in workout_files]

    client = _garmin_client(username, password)

    existing_workouts_by_name = {
        RunningWorkout.extract_workout_name(w): w for w in client.get_workouts()
    }

    for workout in workouts:
        workout_name = workout.get_workout_name()
        existing_workout = existing_workouts_by_name.get(workout_name)

        if existing_workout:
            workout_id = Workout.extract_workout_id(existing_workout)
            workout_owner_id = Workout.extract_workout_owner_id(existing_workout)
            payload = workout.create_workout(workout_id, workout_owner_id)
            logging.info("Updating workout '%s'", workout_name)
            client.update_workout(workout_id, payload)
        else:
            payload = workout.create_workout()
            logging.info("Creating workout '%s'", workout_name)
            client.save_workout(payload)


@app.command(no_args_is_help=True)
def schedule(
    workout_id: Annotated[
        str,
        typer.Argument(help="Garmin Workout ID to be scheduled"),
    ],
    date: Annotated[
        str,
        typer.Argument(
            help="Date on which the workout shall be scheduled, e.g. '2024-04-20'"
        ),
    ],
):
    """
    Schedules a Garmin Workout for a specific date.
    """

    print(f"Scheduling workout {workout_id}  on {date}")
