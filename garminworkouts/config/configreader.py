import yaml
from garminworkouts.config.includeloader import IncludeLoader
from typing import Union
from garminworkouts.models.workout import Workout
from garminworkouts.models.running_workout import (
    RunningWorkout,
    RunningWorkoutConfig,
    WorkoutStep,
)
from garminworkouts.models.duration import Duration

from garminworkouts.models.pace import PaceRange
from pathlib import Path


def read_config(filename: Union[str, Path]) -> dict:
    with open(filename, "r") as f:
        data = yaml.load(f, IncludeLoader)
    return data


def parse_config(config: dict) -> Union[Workout, RunningWorkout]:
    if config["settings"]["sports_type"] == "running":
        zones = [
            PaceRange.from_str(z_name, zone_str)
            for z_name, zone_str in config["settings"]["zones"].items()
        ]
        workout_steps = []
        for step in config["steps"]:
            duration = step.get("duration")
            if duration:
                duration = Duration(duration).to_seconds()
            distance = step.get("distance")
            if distance:
                # TODO: Implement distance parser conversion
                distance = distance

            workout_steps.append(
                WorkoutStep(
                    duration=duration,
                    distance=distance,
                    target=step["target"],
                )
            )

        run_config = RunningWorkoutConfig(
            name=config["name"],
            description=config["description"],
            zones=zones,
            steps=workout_steps,
        )
        return RunningWorkout(run_config)
    else:
        return Workout(config)
